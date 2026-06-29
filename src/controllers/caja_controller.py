from datetime import datetime
from flask import jsonify, request
from models.caja_model import CajaModel
from schemas.caja_schema import AbrirTurnoSchema, CerrarTurnoSchema, MovimientoCajaSchema
from pydantic import ValidationError

class CajaController:
    
    @staticmethod
    def _resumen_turno(turno):
        movimientos = CajaModel.obtener_movimientos_del_turno(turno["id"])
        ventas = CajaModel.obtener_ventas_del_turno(turno["id"])

        saldo_inicial = float(turno.get("saldo_inicial") or 0)
        ventas_efectivo = sum(float(v.get("total") or 0) for v in ventas if v.get("medio_pago") == "EFECTIVO")
        ventas_tarjeta = sum(float(v.get("total") or 0) for v in ventas if v.get("medio_pago") == "TARJETA")
        ventas_yape_plin = sum(float(v.get("total") or 0) for v in ventas if v.get("medio_pago") in ("YAPE", "PLIN"))
        
        ingresos_manuales = sum(float(m.get("monto") or 0) for m in movimientos if m.get("tipo") == "INGRESO")
        egresos_manuales = sum(float(m.get("monto") or 0) for m in movimientos if m.get("tipo") == "EGRESO")
        
        saldo_esperado = saldo_inicial + ventas_efectivo + ingresos_manuales - egresos_manuales

        # 🔥 AQUÍ ESTABA EL ERROR: Me faltaba devolver el flujo para que el JS no explote
        flujo = [{
            "hora": turno.get("fecha_apertura"),
            "tipo": "APERTURA",
            "concepto": "Fondo de caja inicial",
            "monto": saldo_inicial,
        }]

        for venta in ventas:
            if venta.get("medio_pago") == "EFECTIVO":
                flujo.append({
                    "hora": venta.get("fecha_hora"),
                    "tipo": "VENTA_EFECTIVO",
                    "concepto": f"Ticket {venta.get('nro_ticket')}",
                    "monto": float(venta.get("total") or 0),
                })

        for mov in movimientos:
            signo = 1 if mov.get("tipo") == "INGRESO" else -1
            flujo.append({
                "hora": mov.get("registrado_en"),
                "tipo": mov.get("tipo"),
                "concepto": mov.get("concepto"),
                "monto": signo * float(mov.get("monto") or 0),
            })

        flujo.sort(key=lambda item: item.get("hora") or "")

        return {
            "saldo_inicial": round(saldo_inicial, 2),
            "ventas_efectivo": round(ventas_efectivo, 2),
            "ventas_tarjeta": round(ventas_tarjeta, 2),
            "ventas_yape_plin": round(ventas_yape_plin, 2),
            "ingresos_manuales": round(ingresos_manuales, 2),
            "egresos_manuales": round(egresos_manuales, 2),
            "saldo_esperado": round(saldo_esperado, 2),
            "flujo": flujo # <-- Clave para el JS
        }

    @staticmethod
    def abrir_turno():
        try:
            turno_activo = CajaModel.obtener_turno_abierto()
            if turno_activo:
                fecha_apertura = datetime.fromisoformat(turno_activo[0]['fecha_apertura'])
                hoy = datetime.now()
                
                # Regla de Caja Anterior
                if fecha_apertura.date() < hoy.date():
                    return jsonify({
                        "success": False, 
                        "message": "Alerta: Hay una caja del día anterior que nunca se cerró. Por favor, realiza el arqueo y ciérrala antes de abrir una nueva."
                    }), 400
                else:
                    return jsonify({"success": False, "message": "Ya existe una caja abierta hoy."}), 400

            datos_crudos = request.get_json()
            try:
                datos_limpios = AbrirTurnoSchema(**datos_crudos)
            except ValidationError as e:
                return jsonify({"success": False, "message": "Datos inválidos", "data": e.errors()}), 400

            id_usuario_real = request.usuario_actual['id']

            nuevo_turno = {
                "id_usuario": id_usuario_real,
                "fecha_apertura": datetime.now().isoformat(),
                "saldo_inicial": datos_limpios.saldo_inicial,
                "ventas_efectivo": 0, "ingresos_manuales": 0, "egresos_manuales": 0,
                "saldo_esperado": datos_limpios.saldo_inicial,
                "estado": "ABIERTA",
                "observaciones": datos_limpios.observaciones,
            }

            resultado = CajaModel.abrir_turno(nuevo_turno)
            return jsonify({"success": True, "message": "Caja abierta correctamente", "data": resultado[0]}), 201

        except Exception as e:
            return jsonify({"success": False, "message": "Error interno", "data": str(e)}), 500

    @staticmethod
    def cerrar_turno():
        try:
            turnos = CajaModel.obtener_turno_abierto()
            if not turnos:
                return jsonify({"success": False, "message": "No hay una caja abierta para cerrar"}), 400

            turno = turnos[0]
            
            # BLOQUEO DE PROPIETARIO
            if turno['id_usuario'] != request.usuario_actual['id']:
                return jsonify({
                    "success": False, 
                    "message": f"No puedes cerrar la caja de {turno['usuarios']['nombres']}.",
                    "codigo_error": "CAJA_AJENA"
                }), 403

            datos_crudos = request.get_json()
            try:
                datos_limpios = CerrarTurnoSchema(**datos_crudos)
            except ValidationError as e:
                return jsonify({"success": False, "message": "Datos inválidos", "data": e.errors()}), 400

            resumen = CajaController._resumen_turno(turno)
            diferencia = round(datos_limpios.saldo_fisico_real - resumen["saldo_esperado"], 2)

            datos_cierre = {
                "fecha_cierre": datetime.now().isoformat(),
                "ventas_efectivo": resumen["ventas_efectivo"],
                "ingresos_manuales": resumen["ingresos_manuales"],
                "egresos_manuales": resumen["egresos_manuales"],
                "saldo_esperado": resumen["saldo_esperado"],
                "saldo_fisico_real": datos_limpios.saldo_fisico_real,
                "diferencia": diferencia,
                "estado": "CERRADA",
                "observaciones": datos_limpios.observaciones,
            }

            resultado = CajaModel.cerrar_turno(turno["id"], datos_cierre)
            return jsonify({
                "success": True, 
                "message": "Caja cerrada correctamente",
                "data": {"turno": resultado[0], "diferencia": diferencia}
            }), 200

        except Exception as e:
            return jsonify({"success": False, "message": "Error interno", "data": str(e)}), 500

    @staticmethod
    def registrar_movimiento():
        try:
            turnos = CajaModel.obtener_turno_abierto()
            if not turnos:
                return jsonify({"success": False, "message": "No hay caja abierta."}), 400

            turno = turnos[0]
            
            # BLOQUEO DE PROPIETARIO
            if turno['id_usuario'] != request.usuario_actual['id']:
                return jsonify({
                    "success": False, 
                    "message": "No puedes registrar movimientos en la caja de otro usuario.",
                    "codigo_error": "CAJA_AJENA"
                }), 403

            datos_crudos = request.get_json()
            try:
                datos_limpios = MovimientoCajaSchema(**datos_crudos)
            except ValidationError as e:
                return jsonify({"success": False, "message": "Datos inválidos", "data": e.errors()}), 400

            nuevo_movimiento = {
                "id_turno": turno["id"],
                "tipo": datos_limpios.tipo,
                "monto": datos_limpios.monto,
                "concepto": datos_limpios.concepto,
                "registrado_en": datetime.now().isoformat(),
            }

            resultado = CajaModel.registrar_movimiento(nuevo_movimiento)
            return jsonify({"success": True, "message": "Movimiento registrado", "data": resultado[0]}), 201

        except Exception as e:
            return jsonify({"success": False, "message": "Error interno", "data": str(e)}), 500

    @staticmethod
    def obtener_turno_activo():
        try:
            turnos = CajaModel.obtener_turno_abierto()
            if not turnos:
                return jsonify({"success": True, "message": "Caja cerrada", "data": None}), 200

            turno = turnos[0]
            
            # BLOQUEO DE PROPIETARIO (Para que el dashboard del Frontend lo rebote)
            if turno['id_usuario'] != request.usuario_actual['id']:
                nombre_dueño = turno['usuarios']['nombres']
                return jsonify({
                    "success": False, 
                    "message": f"Turno en uso. {nombre_dueño} dejó su caja abierta. Debe cerrarla antes de que puedas usar el módulo.",
                    "codigo_error": "CAJA_AJENA"
                }), 403

            resumen = CajaController._resumen_turno(turno)
            return jsonify({"success": True, "message": "Caja abierta", "data": {"turno": turno, "resumen": resumen}}), 200
        except Exception as e:
            return jsonify({"success": False, "message": "Error interno", "data": str(e)}), 500
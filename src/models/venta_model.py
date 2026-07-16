from config.database import supabase

class VentaModel:

    @staticmethod
    def registrar_venta(datos, id_usuario_real):
        try:
            # === 1. VALIDACIÓN PREVIA DE STOCK (La capa de seguridad) ===
            for item in datos['detalles']:
                prod = supabase.table('productos').select('stock_actual').eq('id', item['id_producto']).execute()
                
                if not prod.data:
                    return {"success": False, "message": f"Producto ID {item['id_producto']} no encontrado"}
                
                stock_actual = prod.data[0]['stock_actual']
                if stock_actual < item['cantidad']:
                    # Aquí retornamos el error que detiene todo el proceso
                    return {"success": False, "message": f"Stock insuficiente para producto ID {item['id_producto']}. Disponible: {stock_actual}"}

            # === 2. GENERACIÓN DE TICKET (Si pasó la validación, procedemos) ===
            # ... (Aquí mantienes tu lógica de generación de ticket que ya tenías)
            res = supabase.table('ventas').select('nro_ticket').order('id', desc=True).limit(1).execute()
            numero = (int(res.data[0]['nro_ticket'].split('-')[1]) + 1) if res.data else 10000
            nuevo_ticket = f"T001-{numero:04d}"

            # === 3. INSERCIÓN DE LA VENTA ===
            subtotal = float(datos['total']) - float(datos['igv'])
            venta = {
                "nro_ticket": nuevo_ticket,
                "id_usuario": id_usuario_real,
                "id_turno": datos.get('id_turno'),
                "subtotal": subtotal,
                "igv": float(datos['igv']),
                "total": float(datos['total']),
                "medio_pago": datos['medio_pago'],
                "monto_entregado": datos.get('monto_entregado', 0.0),
                "vuelto": datos.get('vuelto', 0.0),
                "estado": "VALIDO"
            }
            res_venta = supabase.table('ventas').insert(venta).execute()
            id_venta = res_venta.data[0]['id']

            # === 4. PROCESAR DETALLES Y ACTUALIZAR STOCK ===
            for item in datos['detalles']:
                detalle = {
                    "id_venta": id_venta,
                    "id_producto": item['id_producto'],
                    "cantidad": item['cantidad'],
                    "precio_unitario": float(item['precio_unitario']),
                    "subtotal": float(item['precio_unitario']) * int(item['cantidad'])
                }
                supabase.table('ventas_detalle').insert(detalle).execute()

                # Ahora sí, restamos porque ya validamos que es posible
                prod = supabase.table('productos').select('stock_actual').eq('id', item['id_producto']).execute()
                stock_nuevo = prod.data[0]['stock_actual'] - int(item['cantidad'])
                supabase.table('productos').update({'stock_actual': stock_nuevo}).eq('id', item['id_producto']).execute()

                # Kardex
                supabase.table('kardex').insert({
                    "id_producto": item['id_producto'],
                    "tipo_movimiento": "SALIDA_VENTA",
                    "referencia": nuevo_ticket,
                    "cantidad": -int(item['cantidad']),
                    "saldo_final": stock_nuevo,
                    "id_usuario": id_usuario_real
                }).execute()

            return {"success": True, "message": "Venta registrada correctamente", "data": {"id_venta": id_venta, "nro_ticket": nuevo_ticket}}

        except Exception as e:
            return {"success": False, "message": "Error interno del sistema", "data": str(e)}
from config.database import supabase

class VentaModel:

    @staticmethod
    def registrar_venta(datos, id_usuario_real):
        try:
            # === GENERACIÓN DE TICKET ===
            res = supabase.table('ventas')\
                .select('nro_ticket')\
                .order('id', desc=True)\
                .limit(1).execute()

            if res.data and len(res.data) > 0:
                ultimo_ticket = res.data[0]['nro_ticket']
                try:
                    numero = int(ultimo_ticket.split('-')[1]) + 1
                except:
                    numero = 10000 
            else:
                numero = 10000

            nuevo_ticket = f"T001-{numero:04d}"

            # Verificamos que no exista
            check = supabase.table('ventas').select('id').eq('nro_ticket', nuevo_ticket).execute()
            if check.data:
                nuevo_ticket = f"T001-{numero + 100:04d}"

            # Calcular subtotal
            subtotal = float(datos['total']) - float(datos['igv'])

            # === INSERTAR LA VENTA (AHORA CON ID TURNO Y VUELTO) ===
            venta = {
                "nro_ticket": nuevo_ticket,
                "id_usuario": id_usuario_real,
                "id_turno": datos.get('id_turno'),  # 🔥 LA CONEXIÓN CON LA GAVETA FÍSICA
                "subtotal": subtotal,
                "igv": float(datos['igv']),
                "total": float(datos['total']),
                "medio_pago": datos['medio_pago'],
                "monto_entregado": datos.get('monto_entregado', 0.0), # 🔥 EL DINERO FÍSICO QUE DIO EL CLIENTE
                "vuelto": datos.get('vuelto', 0.0),                   # 🔥 EL CAMBIO QUE LE DIMOS
                "estado": "VALIDO"
            }

            res_venta = supabase.table('ventas').insert(venta).execute()
            id_venta = res_venta.data[0]['id']

            # === PROCESAR DETALLES, STOCK Y KARDEX ===
            for item in datos['detalles']:
                detalle = {
                    "id_venta": id_venta,
                    "id_producto": item['id_producto'],
                    "cantidad": item['cantidad'],
                    "precio_unitario": float(item['precio_unitario']),
                    "subtotal": float(item['precio_unitario']) * int(item['cantidad'])
                }
                supabase.table('ventas_detalle').insert(detalle).execute()

                # Reducir stock
                prod = supabase.table('productos').select('stock_actual').eq('id', item['id_producto']).execute()

                if prod.data:
                    stock_nuevo = max(0, prod.data[0]['stock_actual'] - int(item['cantidad']))
                    supabase.table('productos').update({'stock_actual': stock_nuevo}).eq('id', item['id_producto']).execute()

                # Kardex con el ID REAL del token
                kardex = {
                    "id_producto": item['id_producto'],
                    "tipo_movimiento": "SALIDA_VENTA",
                    "referencia": nuevo_ticket,
                    "cantidad": -int(item['cantidad']),
                    "saldo_final": stock_nuevo if prod.data else 0,
                    "id_usuario": id_usuario_real
                }
                supabase.table('kardex').insert(kardex).execute()

            # Formato de respuesta universal
            return {
                "success": True,
                "message": "Venta registrada correctamente",
                "data": {
                    "id_venta": id_venta,
                    "nro_ticket": nuevo_ticket
                }
            }

        except Exception as e:
            return {
                "success": False, 
                "message": "Error al guardar en la base de datos", 
                "data": str(e)
            }
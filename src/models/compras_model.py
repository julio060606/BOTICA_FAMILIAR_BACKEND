from config.database import supabase
from datetime import datetime


class CompraModel:

    @staticmethod
    def registrar_ingreso(datos):
        # 1. Insertamos la cabecera en 'compras'
        cabecera = {
            "id_proveedor": datos['id_proveedor'],
            "id_usuario": datos['id_usuario'],  # El usuario que está en el sistema
            "nro_documento": datos['nro_documento'],
            "fecha_emision": datos['fecha_emision'],
            "total": datos['total']
        }
        res_compra = supabase.table('compras').insert(cabecera).execute()
        id_compra = res_compra.data[0]['id']  # Capturamos el ID que se acaba de crear

        # 2. Recorremos los productos que mandó el frontend
        for item in datos['detalles']:
            # A) Guardar en compras_detalle
            detalle = {
                "id_compra": id_compra,
                "id_producto": item['id_producto'],
                "codigo_lote": item['codigo_lote'],
                "fecha_vencimiento": item['fecha_vencimiento'],
                "cantidad": item['cantidad'],
                "costo_unitario": item['costo_unitario'],
                "subtotal": item['subtotal']
            }
            supabase.table('compras_detalle').insert(detalle).execute()

            # B) Crear el Lote en lotes_stock
            lote = {
                "id_producto": item['id_producto'],
                "codigo_lote": item['codigo_lote'],
                "fecha_vencimiento": item['fecha_vencimiento'],
                "stock_restante": item['cantidad']
            }
            supabase.table('lotes_stock').insert(lote).execute()

            # C) Actualizar el stock_actual y el precio_costo en la tabla productos
            # Primero leemos cuánto stock tiene ahora
            res_prod = supabase.table('productos').select('stock_actual').eq('id', item['id_producto']).execute()
            stock_viejo = res_prod.data[0]['stock_actual']
            stock_nuevo = stock_viejo + item['cantidad']

            # Hacemos el UPDATE (AQUÍ ESTÁ LA MAGIA: Agregamos el precio_costo)
            supabase.table('productos').update({
                'stock_actual': stock_nuevo,
                'precio_costo': item['costo_unitario']  # <--- Esto actualiza el catálogo
            }).eq('id', item['id_producto']).execute()

            # D) Registrar en el Kardex
            kardex_registro = {
                "id_producto": item['id_producto'],
                "tipo_movimiento": "ENTRADA_COMPRA",
                "referencia": f"Factura {datos['nro_documento']}",
                "cantidad": item['cantidad'],
                "saldo_final": stock_nuevo,
                "id_usuario": datos['id_usuario']
            }
            supabase.table('kardex').insert(kardex_registro).execute()

        return {"mensaje": "Ingreso registrado correctamente, stock y kardex actualizados", "id_compra": id_compra}
from config.database import supabase
from datetime import datetime, timedelta


class NotificacionModel:

    @staticmethod
    def obtener_alertas_stock():
        # Traemos todos los productos activos
        res = supabase.table('productos') \
            .select('id, sku, nombre, stock_actual, stock_minimo') \
            .eq('estado', 'ACTIVO') \
            .execute()

        productos = res.data
        alertas = []

        for p in productos:
            # Si el stock cayó por debajo de la alerta de la botica
            if p['stock_actual'] <= p['stock_minimo']:
                nivel = "CRITICO" if p['stock_actual'] == 0 else "ADVERTENCIA"
                alertas.append({
                    "id": f"stock_{p['id']}",
                    "tipo": "STOCK",
                    "nivel": nivel,
                    "titulo": "Stock Bajo" if nivel == "ADVERTENCIA" else "Stock Agotado",
                    "mensaje": f"{p['nombre']} tiene {p['stock_actual']} unds. (Mínimo: {p['stock_minimo']})",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        return alertas

    @staticmethod
    def obtener_alertas_vencimiento():
        hoy = datetime.now().date()
        limite_90_dias = hoy + timedelta(days=90)

        # Revisamos los lotes que entraron en las compras
        # (En una versión más avanzada, leeríamos de la tabla lotes_stock)
        res = supabase.table('compras_detalle') \
            .select('*, productos(nombre)') \
            .lte('fecha_vencimiento', str(limite_90_dias)) \
            .execute()

        alertas = []

        for lote in res.data:
            # Convertimos la fecha de texto (SQL) a fecha de Python
            fecha_v = datetime.strptime(lote['fecha_vencimiento'], '%Y-%m-%d').date()
            nombre_prod = lote['productos']['nombre'] if lote['productos'] else 'Desconocido'

            if fecha_v < hoy:
                alertas.append({
                    "id": f"venc_{lote['id']}",
                    "tipo": "VENCIMIENTO",
                    "nivel": "CRITICO",
                    "titulo": "Producto Vencido",
                    "mensaje": f"{nombre_prod} (Lote: {lote['codigo_lote']}) venció el {fecha_v.strftime('%d/%m/%Y')}",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                dias_restantes = (fecha_v - hoy).days
                alertas.append({
                    "id": f"venc_{lote['id']}",
                    "tipo": "VENCIMIENTO",
                    "nivel": "ADVERTENCIA",
                    "titulo": "Próximo a Vencer",
                    "mensaje": f"{nombre_prod} (Lote: {lote['codigo_lote']}) vence en {dias_restantes} días.",
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

        return alertas
from config.database import supabase

class TicketVentaModel:

    @staticmethod
    def crear_ticket(datos):
        """Inserta un nuevo ticket de venta en la tabla 'ventas'"""
        respuesta = supabase.table('ventas').insert(datos).execute()
        return respuesta.data

    @staticmethod
    def obtener_historial(limit=50):
        """Obtiene historial de ventas ordenado por fecha"""
        respuesta = supabase.table('ventas') \
            .select("*") \
            .order('fecha_hora', desc=True) \
            .limit(limit) \
            .execute()
        return respuesta.data

    @staticmethod
    def obtener_ticket_por_id(ticket_id):
        """Obtiene una venta específica por su ID"""
        respuesta = supabase.table('ventas') \
            .select("*") \
            .eq('id', ticket_id) \
            .execute()
        return respuesta.data

    @staticmethod
    def buscar_por_metodo_pago(medio_pago, limit=30):
        """Filtra ventas por medio de pago (ej. EFECTIVO, YAPE)"""
        respuesta = supabase.table('ventas') \
            .select("*") \
            .eq('medio_pago', medio_pago) \
            .order('fecha_hora', desc=True) \
            .limit(limit) \
            .execute()
        return respuesta.data
from config.database import supabase

class KardexModel:

    @staticmethod
    def obtener_movimientos(id_producto):
        # Buscamos en el kardex donde el id coincida, y lo ordenamos por fecha descendente
        respuesta = supabase.table('kardex')\
            .select('*, usuarios(nombres)')\
            .eq('id_producto', id_producto)\
            .order('fecha_hora', desc=True)\
            .execute()
        return respuesta.data
from config.database import supabase

class ProductoModel:

    @staticmethod
    def obtener_todos():
        # Vamos a Supabase y traemos todos los registros de la tabla 'productos'
        respuesta = supabase.table('productos').select('*').execute()
        return respuesta.data

    @staticmethod
    def crear(datos):
        pass  # Este lo dejamos vacío para que tu compañero lo programe después
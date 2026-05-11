from config.database import supabase

class ProductoModel:

    @staticmethod
    def obtener_todos():
        # Traemos los productos ordenados del más nuevo al más antiguo
        respuesta = supabase.table('productos').select('*, categorias(nombre)').order('id', desc=True).execute()
        return respuesta.data

    @staticmethod
    def crear(datos):
        respuesta = supabase.table('productos').insert(datos).execute()
        return respuesta.data

    @staticmethod
    def actualizar(id_producto, datos):
        # Actualizamos un producto específico por su ID
        respuesta = supabase.table('productos').update(datos).eq('id', id_producto).execute()
        return respuesta.data
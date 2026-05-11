from config.database import supabase


class CategoriaModel:

    @staticmethod
    def obtener_todas():
        # Trae todas las categorías ordenadas alfabéticamente
        respuesta = supabase.table('categorias').select('*').order('nombre').execute()
        return respuesta.data
from config.database import supabase

class ProveedorModel:
    @staticmethod
    def obtener_todos():
        respuesta = supabase.table('proveedores').select('*').order('razon_social').execute()
        return respuesta.data
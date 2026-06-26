from config.database import supabase

class AuthModel:
    @staticmethod
    def buscar_por_username(username):
        """Busca un usuario en la tabla para verificar sus credenciales"""
        respuesta = supabase.table('usuarios') \
            .select("*") \
            .eq('username', username) \
            .execute()
        
        # Si la lista tiene datos, devolvemos el primer usuario. Si no, None.
        return respuesta.data[0] if respuesta.data else None
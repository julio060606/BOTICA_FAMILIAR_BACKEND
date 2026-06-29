from config.database import supabase


class CajaModel:
    @staticmethod
    def abrir_turno(datos):
        respuesta = supabase.table("caja_turnos").insert(datos).execute()
        return respuesta.data

    @staticmethod
    def obtener_turno_abierto():
        respuesta = (
            supabase.table("caja_turnos")
            .select("*, usuarios(nombres, username, rol)")
            .eq("estado", "ABIERTA")
            .order("fecha_apertura", desc=True)
            .limit(1)
            .execute()
        )
        return respuesta.data

    @staticmethod
    def obtener_turno_por_id(id_turno):
        respuesta = (
            supabase.table("caja_turnos")
            .select("*, usuarios(nombres, username, rol)")
            .eq("id", id_turno)
            .execute()
        )
        return respuesta.data

    @staticmethod
    def cerrar_turno(id_turno, datos_cierre):
        respuesta = (
            supabase.table("caja_turnos")
            .update(datos_cierre)
            .eq("id", id_turno)
            .execute()
        )
        return respuesta.data

    @staticmethod
    def actualizar_totales_turno(id_turno, datos):
        respuesta = (
            supabase.table("caja_turnos")
            .update(datos)
            .eq("id", id_turno)
            .execute()
        )
        return respuesta.data

    @staticmethod
    def obtener_historial_turnos(limit=20):
        respuesta = (
            supabase.table("caja_turnos")
            .select("*, usuarios(nombres, username, rol)")
            .order("fecha_apertura", desc=True)
            .limit(limit)
            .execute()
        )
        return respuesta.data

    @staticmethod
    def registrar_movimiento(datos):
        respuesta = supabase.table("caja_movimientos").insert(datos).execute()
        return respuesta.data

    @staticmethod
    def obtener_movimientos_del_turno(id_turno):
        respuesta = (
            supabase.table("caja_movimientos")
            .select("*")
            .eq("id_turno", id_turno)
            .order("registrado_en", desc=False)
            .execute()
        )
        return respuesta.data

    @staticmethod
    def obtener_ventas_del_turno(id_turno):
        respuesta = (
            supabase.table("ventas")
            .select("id, nro_ticket, total, medio_pago, estado, fecha_hora")
            .eq("id_turno", id_turno)
            .eq("estado", "VALIDO")
            .order("fecha_hora", desc=False)
            .execute()
        )
        return respuesta.data

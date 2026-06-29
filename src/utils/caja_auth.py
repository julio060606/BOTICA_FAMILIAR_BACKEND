from functools import wraps
from flask import jsonify, request
from models.caja_model import CajaModel

def requiere_caja_abierta(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        turno = CajaModel.obtener_turno_abierto()
        
        if not turno:
            return jsonify({
                "success": False, 
                "message": "Operación bloqueada. Debes abrir la caja primero.",
                "codigo_error": "CAJA_CERRADA"
            }), 403
            
        id_usuario_logueado = request.usuario_actual['id']
        dueño_caja_id = turno[0]['id_usuario']
        
        if id_usuario_logueado != dueño_caja_id:
            nombre_dueño = turno[0]['usuarios']['nombres']
            return jsonify({
                "success": False, 
                "message": f"Acceso denegado. {nombre_dueño} dejó su caja abierta. Debe cerrarla antes de que puedas operar.",
                "codigo_error": "CAJA_AJENA"
            }), 403
            
        # 🔥 LA LÍNEA MÁGICA: Le pasamos el ID del turno al controlador de ventas
        request.id_turno_actual = turno[0]['id']
            
        return f(*args, **kwargs)
    return decorated_function
import jwt
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "super_secreto_botica_familiar"

def token_requerido(roles_permitidos=None):
    def decorador(f):
        @wraps(f)
        def funcion_decorada(*args, **kwargs):
            token = None
            
            # 1. Capturar el token del Header
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(" ")[1]

            # 2. ERROR 401: El Frontend no envió la credencial
            if not token:
                return jsonify({
                    "success": False, 
                    "message": "Acceso denegado: Falla el token de acceso"
                }), 401

            try:
                # 3. Leer la credencial
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                usuario_rol = data['rol']

                # 4. ERROR 403: Tiene token, pero no tiene el ROL necesario
                if roles_permitidos and usuario_rol not in roles_permitidos:
                    return jsonify({
                        "success": False, 
                        "message": f"Acceso denegado: Se requiere rol {roles_permitidos}"
                    }), 403

                # Si todo está bien, inyectamos los datos del usuario en el request 
                # por si el controlador quiere saber quién hizo la acción
                request.usuario_actual = data

            except jwt.ExpiredSignatureError:
                return jsonify({"success": False, "message": "El token expiró. Inicie sesión de nuevo."}), 401
            except jwt.InvalidTokenError:
                return jsonify({"success": False, "message": "Token inválido o corrupto."}), 401

            # 5. Todo en orden, pasamos a la ruta original
            return f(*args, **kwargs)
        return funcion_decorada
    return decorador
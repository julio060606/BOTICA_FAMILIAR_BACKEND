import jwt
import datetime
from flask import request, jsonify
from models.auth_model import AuthModel

# Llave secreta para firmar el token (LUEGO LO PASAREMOS A UN ARCHIVO .env)
SECRET_KEY = "super_secreto_botica_familiar"

class AuthController:
    @staticmethod
    def login():
        try:
            datos = request.get_json()
            username = datos.get('username')
            password = datos.get('password')

            if not username or not password:
                return jsonify({"success": False, "message": "Faltan credenciales"}), 400

            # 1. Buscar usuario en Supabase
            usuario = AuthModel.buscar_por_username(username)

            # 2. Verificar si existe y si la contraseña coincide
            # (⚠️ NOTA: Aquí haremos el cambio a bcrypt más adelante)
            if not usuario or usuario['password_hash'] != password:
                return jsonify({"success": False, "message": "Usuario o contraseña incorrectos"}), 401
            
            # 3. Verificar si el usuario está activo
            if usuario['estado'] != 'ACTIVO':
                return jsonify({"success": False, "message": "Usuario inactivo"}), 403

            # 4. Fabricar el JWT (La credencial)
            payload = {
                "id": usuario['id'],
                "username": usuario['username'],
                "rol": usuario['rol'],
                # El token expira en 8 horas (un turno de trabajo normal)
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            # 5. Responder con la Estructura Universal
            return jsonify({
                "success": True,
                "message": "Login exitoso",
                "data": {
                    "token": token,
                    "usuario": {
                        "nombres": usuario['nombres'],
                        "rol": usuario['rol']
                    }
                }
            }), 200

        except Exception as e:
            return jsonify({"success": False, "message": "Error interno", "data": str(e)}), 500
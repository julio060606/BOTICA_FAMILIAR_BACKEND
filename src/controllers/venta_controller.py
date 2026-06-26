from flask import jsonify, request
from models.venta_model import VentaModel
from schemas.venta_schema import VentaSchema
from pydantic import ValidationError

class VentasController:

    @staticmethod
    def registrar_venta():
        try:
            datos_crudos = request.get_json()

            # 1. Validación estricta con Pydantic
            try:
                datos_limpios = VentaSchema(**datos_crudos)
            except ValidationError as error:
                return jsonify({
                    "success": False, 
                    "message": "Error de validación en los datos enviados", 
                    "data": error.errors()
                }), 400

            # 2. Seguridad Zero Trust: Sacamos el ID del token verificado
            # (Recordemos que request.usuario_actual lo inyecta nuestro utils/auth.py)
            id_usuario_real = request.usuario_actual['id']

            # 3. Enviamos los datos limpios (.model_dump() o .dict()) al modelo
            resultado = VentaModel.registrar_venta(datos_limpios.model_dump(), id_usuario_real)

            if resultado.get("success"):
                return jsonify(resultado), 201
            else:
                return jsonify(resultado), 400

        except Exception as e:
            return jsonify({
                "success": False, 
                "message": "Error interno del servidor", 
                "data": str(e)
            }), 500
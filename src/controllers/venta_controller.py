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
                return jsonify({"success": False, "message": "Datos inválidos", "data": error.errors()}), 400

            # 2. Seguridad Zero Trust (Sacamos ID de Usuario y ID de Caja)
            id_usuario_real = request.usuario_actual['id']
            
            # 🔥 ATRAPAMOS EL TURNO QUE NOS PASÓ EL GUARDIA
            id_turno_real = getattr(request, 'id_turno_actual', None)

            # 3. Preparamos el paquete inyectando el id_turno
            datos_para_guardar = datos_limpios.model_dump()
            datos_para_guardar['id_turno'] = id_turno_real

            # 4. Lo enviamos al modelo
            resultado = VentaModel.registrar_venta(datos_para_guardar, id_usuario_real)

            if resultado.get("success"):
                return jsonify(resultado), 201
            else:
                return jsonify(resultado), 400

        except Exception as e:
            return jsonify({"success": False, "message": "Error interno", "data": str(e)}), 500
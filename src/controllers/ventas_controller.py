from flask import jsonify, request
from models.venta_model import VentaModel


class VentasController:

    @staticmethod
    def registrar_venta():
        try:
            datos = request.get_json()
            resultado = VentaModel.registrar_venta(datos)

            if resultado.get("success"):
                return jsonify(resultado), 201
            else:
                return jsonify(resultado), 400

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

from flask import jsonify, request
from models.proveedor_model import ProveedorModel
from models.compras_model import CompraModel


class ComprasController:

    @staticmethod
    def obtener_proveedores():
        try:
            proveedores = ProveedorModel.obtener_todos()
            return jsonify(proveedores), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def guardar_ingreso():
        try:
            datos = request.get_json()
            # Llamamos a tu mega-función del modelo
            resultado = CompraModel.registrar_ingreso(datos)
            return jsonify(resultado), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
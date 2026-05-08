from flask import jsonify
from models.producto_model import ProductoModel


class InventarioController:

    @staticmethod
    def obtener_catalogo():
        try:
            # 1. El controlador llama al modelo
            productos = ProductoModel.obtener_todos()
            # 2. Empaqueta los datos en JSON y los envía
            return jsonify(productos), 200
        except Exception as e:
            # Si algo falla (ej. la tabla no existe), nos avisa
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def agregar_producto():
        pass
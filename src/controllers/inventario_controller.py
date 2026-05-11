from flask import jsonify, request
from models.producto_model import ProductoModel
from models.categoria_model import CategoriaModel


class InventarioController:

    @staticmethod
    def obtener_catalogo():
        try:
            productos = ProductoModel.obtener_todos()
            return jsonify(productos), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def obtener_categorias():
        try:
            categorias = CategoriaModel.obtener_todas()
            return jsonify(categorias), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def agregar_producto():
        try:
            # Capturamos los datos que envía tu formulario HTML
            datos = request.get_json()

            # Mandamos a crear el producto a Supabase
            nuevo_producto = ProductoModel.crear(datos)

            return jsonify({
                "mensaje": "Producto creado con éxito",
                "producto": nuevo_producto
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def actualizar_producto(id_producto):
        try:
            datos = request.get_json()
            resultado = ProductoModel.actualizar(id_producto, datos)
            return jsonify({"mensaje": "Producto actualizado", "producto": resultado}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
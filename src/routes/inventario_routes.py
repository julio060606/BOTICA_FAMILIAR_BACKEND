from flask import Blueprint
from controllers.inventario_controller import InventarioController
from utils.auth import token_requerido  # <-- Traemos a nuestro guardia

inventario_bp = Blueprint('inventario', __name__)

inventario_bp.route('/categorias', methods=['GET'])(InventarioController.obtener_categorias)

inventario_bp.route('/productos', methods=['GET'])(InventarioController.obtener_catalogo)
inventario_bp.route('/productos', methods=['POST'])(InventarioController.agregar_producto)
inventario_bp.route('/productos/<int:id_producto>', methods=['PUT'])(InventarioController.actualizar_producto)
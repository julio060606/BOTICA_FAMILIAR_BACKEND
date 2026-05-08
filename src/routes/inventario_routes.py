from flask import Blueprint
from controllers.invetario_controller import InventarioController

# Creamos el Blueprint
inventario_bp = Blueprint('inventario', __name__)

# Rutas vacías listas para ser enlazadas
inventario_bp.route('/productos', methods=['GET'])(InventarioController.obtener_catalogo)
inventario_bp.route('/productos', methods=['POST'])(InventarioController.agregar_producto)
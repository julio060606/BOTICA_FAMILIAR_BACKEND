from flask import Blueprint
from controllers.compras_controller import ComprasController

compras_bp = Blueprint('compras', __name__)

compras_bp.route('/proveedores', methods=['GET'])(ComprasController.obtener_proveedores)
compras_bp.route('/ingresar', methods=['POST'])(ComprasController.guardar_ingreso)
from flask import Blueprint
from controllers.venta_controller import VentasController
from utils.auth import token_requerido

ventas_bp = Blueprint('ventas', __name__)

# Ruta para registrar una venta desde el POS
@ventas_bp.route('/registrar', methods=['POST'])
@token_requerido(roles_permitidos=['ADMIN']) # <-- El candado
def registrar_venta():
    return VentasController.registrar_venta()
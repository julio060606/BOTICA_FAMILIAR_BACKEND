from flask import Blueprint
from controllers.ventas_controller import VentasController

ventas_bp = Blueprint('ventas', __name__)

# Ruta para registrar una venta desde el POS
ventas_bp.route('/registrar', methods=['POST'])(VentasController.registrar_venta)

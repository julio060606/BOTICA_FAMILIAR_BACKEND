from flask import Blueprint
from controllers.kardex_controller import KardexController

# Creamos el Blueprint exclusivo para el Kardex
kardex_bp = Blueprint('kardex', __name__)

# La ruta principal del kardex.
# Como en app.py le daremos el prefijo '/api/kardex', aquí solo ponemos '/<int:id_producto>'
kardex_bp.route('/<int:id_producto>', methods=['GET'])(KardexController.ver_historial)
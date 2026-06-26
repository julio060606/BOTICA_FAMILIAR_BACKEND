from flask import Blueprint
from controllers.kardex_controller import KardexController
from utils.auth import token_requerido  # <-- Traemos a nuestro guardia

# Creamos el Blueprint exclusivo para el Kardex
kardex_bp = Blueprint('kardex', __name__)

# ==================== RUTAS PROTEGIDAS ====================

@kardex_bp.route('/<int:id_producto>', methods=['GET'])
@token_requerido(roles_permitidos=['ADMIN'])
def ver_historial(id_producto):
    return KardexController.ver_historial(id_producto)
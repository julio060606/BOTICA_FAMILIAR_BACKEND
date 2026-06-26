from flask import Blueprint
from controllers.notificacion_controller import NotificacionController
from utils.auth import token_requerido  # <-- Traemos a nuestro guardia

notificacion_bp = Blueprint('notificaciones', __name__)

notificacion_bp.route('/', methods=['GET'])(NotificacionController.obtener_todas)
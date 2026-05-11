from flask import Blueprint
from controllers.notificacion_controller import NotificacionController

notificacion_bp = Blueprint('notificaciones', __name__)

notificacion_bp.route('/', methods=['GET'])(NotificacionController.obtener_todas)
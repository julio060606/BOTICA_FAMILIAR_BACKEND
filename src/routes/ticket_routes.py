from flask import Blueprint
from controllers.ticket_controller import TicketController

# Creación del Blueprint
ticket_bp = Blueprint('ticket', __name__)

# ==================== RUTAS (Endpoints) ====================

ticket_bp.route('/', methods=['POST'])(TicketController.crear_ticket)
ticket_bp.route('/', methods=['GET'])(TicketController.obtener_historial)
ticket_bp.route('/<int:ticket_id>', methods=['GET'])(TicketController.obtener_ticket)
ticket_bp.route('/metodo-pago/<string:metodo>', methods=['GET'])(TicketController.buscar_por_metodo_pago)
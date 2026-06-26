from flask import Blueprint
from controllers.ticket_controller import TicketController
from utils.auth import token_requerido  # <-- IMPORTAMOS EL GUARDIA

ticket_bp = Blueprint('ticket', __name__)

# ==================== RUTAS PROTEGIDAS ====================

# Solo ADMIN y CAJERO pueden registrar ventas
@ticket_bp.route('/', methods=['POST'])
@token_requerido(roles_permitidos=['ADMIN', 'CAJERO'])
def crear_ticket():
    return TicketController.crear_ticket()

# Cualquiera del personal puede ver el historial
@ticket_bp.route('/', methods=['GET'])
@token_requerido(roles_permitidos=['ADMIN', 'CAJERO'])
def obtener_historial():
    return TicketController.obtener_historial()

# ¡EJEMPLO DE SEGURIDAD ESTRICTA!
# Solo el ADMIN podría, por ejemplo, anular un ticket (Ruta ficticia para ejemplo)
@ticket_bp.route('/anular/<int:ticket_id>', methods=['POST'])
@token_requerido(roles_permitidos=['ADMIN'])
def anular_ticket(ticket_id):
    return TicketController.anular_ticket(ticket_id)


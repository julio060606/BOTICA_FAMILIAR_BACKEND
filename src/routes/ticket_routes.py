from flask import Blueprint
from controllers.ticket_controller import TicketController
from utils.auth import token_requerido

ticket_bp = Blueprint('ticket', __name__)

# Registrar venta
@ticket_bp.route('/', methods=['POST'])
@token_requerido(roles_permitidos=['ADMIN', 'CAJERO'])
def crear_ticket():
    return TicketController.crear_ticket()

# Ver historial completo de la tabla
@ticket_bp.route('/', methods=['GET'])
@token_requerido(roles_permitidos=['ADMIN', 'CAJERO'])
def obtener_historial():
    return TicketController.obtener_historial()

# 🔥 NUEVA RUTA: Para cargar los productos del modal de previsualización
@ticket_bp.route('/<int:ticket_id>/productos', methods=['GET'])
@token_requerido(roles_permitidos=['ADMIN', 'CAJERO'])
def obtener_detalle_productos(ticket_id):
    return TicketController.obtener_detalle_productos(ticket_id)

# Ruta de ejemplo para el Admin
@ticket_bp.route('/anular/<int:ticket_id>', methods=['POST'])
@token_requerido(roles_permitidos=['ADMIN'])
def anular_ticket(ticket_id):
    return TicketController.anular_ticket(ticket_id)

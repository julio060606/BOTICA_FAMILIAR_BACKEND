from flask import Blueprint
from controllers.caja_controller import CajaController
from utils.auth import token_requerido # <-- Importamos tu escudo base

caja_bp = Blueprint("caja", __name__)

# Solo ADMIN y CAJERO pueden operar la caja
@caja_bp.route("/turno/abrir", methods=["POST"])
@token_requerido(roles_permitidos=['ADMIN', 'CAJERO'])
def abrir_turno():
    return CajaController.abrir_turno()

@caja_bp.route("/turno/activo", methods=["GET"])
@token_requerido(roles_permitidos=['ADMIN', 'CAJERO'])
def obtener_turno_activo():
    return CajaController.obtener_turno_activo()

@caja_bp.route("/turno/cerrar", methods=["POST"])
@token_requerido(roles_permitidos=['ADMIN', 'CAJERO'])
def cerrar_turno():
    return CajaController.cerrar_turno()

@caja_bp.route("/movimiento", methods=["POST"])
@token_requerido(roles_permitidos=['ADMIN', 'CAJERO'])
def registrar_movimiento():
    return CajaController.registrar_movimiento()

# El historial de turnos (Auditoría) usualmente solo lo ve el ADMIN
@caja_bp.route("/historial", methods=["GET"])
@token_requerido(roles_permitidos=['ADMIN'])
def obtener_historial_turnos():
    return CajaController.obtener_historial_turnos()
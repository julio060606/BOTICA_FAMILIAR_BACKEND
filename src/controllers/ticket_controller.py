from flask import request, jsonify
from pydantic import ValidationError
from schemas.ticket_schema import TicketVentaSchema
from models.ticket_model import TicketVentaModel

class TicketController:

    @staticmethod
    def crear_ticket():
        try:
            datos_crudos = request.get_json()
            datos_seguros = TicketVentaSchema(**datos_crudos).model_dump()
            
            resultado = TicketVentaModel.crear_ticket(datos_seguros)
            return jsonify({"success": True, "mensaje": "Ticket registrado con éxito", "data": resultado}), 201
            
        except ValidationError as e:
            errores = [{"campo": err["loc"][0], "mensaje": err["msg"]} for err in e.errors()]
            return jsonify({"success": False, "error": "Fallo en la validación de datos", "detalles": errores}), 400
            
        except Exception as e:
            return jsonify({"success": False, "error": "Error interno del servidor", "detalle": str(e)}), 500

    @staticmethod
    def obtener_historial():
        try:
            limit = request.args.get('limit', 50, type=int)
            tickets = TicketVentaModel.obtener_historial(limit)
            # Estandarizamos la respuesta para que el JS sepa si fue exitoso
            return jsonify({"success": True, "data": tickets}), 200
        except Exception as e:
            return jsonify({"success": False, "error": "Error interno del servidor", "detalle": str(e)}), 500

    @staticmethod
    def obtener_ticket(ticket_id):
        try:
            ticket = TicketVentaModel.obtener_ticket_por_id(ticket_id)
            if ticket:
                return jsonify({"success": True, "data": ticket[0]}), 200
            return jsonify({"success": False, "error": "Ticket no encontrado"}), 404
        except Exception as e:
            return jsonify({"success": False, "error": "Error interno del servidor"}), 500

    # 🔥 NUEVO MÉTODO: Despacha la lista de artículos para el modal del frontend
    @staticmethod
    def obtener_detalle_productos(ticket_id):
        try:
            productos = TicketVentaModel.obtener_detalle_productos(ticket_id)
            return jsonify({"success": True, "data": productos}), 200
        except Exception as e:
            return jsonify({"success": False, "error": "Error interno del servidor", "detalle": str(e)}), 500

    @staticmethod
    def buscar_por_metodo_pago(metodo):
        try:
            tickets = TicketVentaModel.buscar_por_metodo_pago(metodo.upper())
            return jsonify({"success": True, "data": tickets}), 200
        except Exception as e:
            return jsonify({"success": False, "error": "Error interno del servidor"}), 500
from flask import jsonify
from models.notificacion_model import NotificacionModel


class NotificacionController:

    @staticmethod
    def obtener_todas():
        try:
            # Calculamos las alertas en tiempo real
            alertas_stock = NotificacionModel.obtener_alertas_stock()
            alertas_vencimiento = NotificacionModel.obtener_alertas_vencimiento()

            # Las unimos en una sola lista
            todas_las_alertas = alertas_stock + alertas_vencimiento

            # (Opcional) Las ordenamos para que los CRÍTICOS salgan primero
            todas_las_alertas.sort(key=lambda x: 0 if x['nivel'] == 'CRITICO' else 1)

            return jsonify({
                "total": len(todas_las_alertas),
                "criticas": sum(1 for a in todas_las_alertas if a['nivel'] == 'CRITICO'),
                "advertencias": sum(1 for a in todas_las_alertas if a['nivel'] == 'ADVERTENCIA'),
                "alertas": todas_las_alertas
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
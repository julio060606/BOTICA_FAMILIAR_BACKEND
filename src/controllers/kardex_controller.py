from flask import jsonify
from models.kardex_model import KardexModel


class KardexController:

    @staticmethod
    def ver_historial(id_producto):
        try:
            movimientos = KardexModel.obtener_movimientos(id_producto)

            if not movimientos:
                return jsonify({"mensaje": "Este producto aún no tiene movimientos"}), 404

            return jsonify(movimientos), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
from flask import Flask
from flask_cors import CORS
from src.config.database import supabase


def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def index():
        try:
            # 1. Intentamos conectarnos a Supabase y traer los datos de tu botica
            respuesta = supabase.table('empresa').select('*').execute()

            # 2. Si funciona, mostramos los datos en la pantalla
            return {
                "status": "online",
                "message": "¡Conexión a Supabase EXITOSA! 🚀",
                "datos_de_tu_bd": respuesta.data
            }
        except Exception as e:
            # 3. Si las claves están mal o no hay tablas, capturamos el error real
            return {
                "status": "error",
                "message": "Flask encendió, pero Supabase rechazó la conexión ❌",
                "detalle_del_error": str(e)
            }

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
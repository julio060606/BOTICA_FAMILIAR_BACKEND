from flask import Flask
from flask_cors import CORS
# Importamos la ruta de tu módulo
from routes.inventario_routes import inventario_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Aquí es donde le pegamos la etiqueta "/api/inventario" a todas tus rutas de ese archivo
    app.register_blueprint(inventario_bp, url_prefix='/api/inventario')

    # La ruta principal, limpia y sencilla
    @app.route('/')
    def index():
        return {"status": "online", "message": "API de Botica Familiar conectada 🚀"}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
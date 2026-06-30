from flask import Flask
from flask_cors import CORS

# ==========================================
# 1. IMPORTACIÓN DE RUTAS (Todos los módulos)
# ==========================================
from routes.inventario_routes import inventario_bp
from routes.compras_routes import compras_bp
from routes.kardex_routes import kardex_bp
from routes.notificacion_routes import notificacion_bp
from routes.ticket_routes import ticket_bp
from routes.auth_routes import auth_bp
from routes.venta_routes import ventas_bp
from routes.caja_routes import caja_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # ==========================================
    # 2. REGISTRO DE BLUEPRINTS (Las Etiquetas)
    # ==========================================
    app.register_blueprint(inventario_bp, url_prefix='/api/inventario')
    app.register_blueprint(compras_bp, url_prefix='/api/compras')
    app.register_blueprint(kardex_bp, url_prefix='/api/kardex')
    app.register_blueprint(notificacion_bp, url_prefix='/api/notificaciones')
    app.register_blueprint(ticket_bp, url_prefix='/api/ticket')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(ventas_bp, url_prefix='/api/ventas')  # ← Nueva línea
    app.register_blueprint(caja_bp, url_prefix='/api/caja')  # ← Nueva línea
    
    
    # Ruta de bienvenida para saber que el motor está encendido
    @app.route('/')
    def index():
        return {"status": "online", "message": "API de Botica Familiar conectada 🚀"}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
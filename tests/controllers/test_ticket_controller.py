import pytest
from src.app import create_app

# 1. Configuración del "Navegador de Pruebas" de Flask (Fixture)
@pytest.fixture
def cliente_web():
    """Crea un servidor Flask falso en memoria para probar las rutas"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ====================================================================
# PRUEBAS DEL CONTROLADOR (Simulando a Thunder Client)
# ====================================================================

def test_crear_ticket_rechaza_datos_incompletos(cliente_web):
    """Prueba que Pydantic bloquea un JSON si le falta el 'total'"""
    
    # Simulamos un JSON malo (falta el campo 'total')
    json_malo = {
        "numero_ticket": "T001-8888",
        "metodo_pago": "EFECTIVO",
        "id_cajero": 1
    }
    
    # Hacemos la petición POST virtual a nuestra ruta
    respuesta = cliente_web.post('/api/tickets/', json=json_malo)
    
    # Verificaciones:
    assert respuesta.status_code == 400 # Pydantic debe responder Bad Request
    datos_respuesta = respuesta.get_json()
    assert "Fallo en la validación" in datos_respuesta["error"]

def test_crear_ticket_rechaza_metodo_pago_invalido(cliente_web):
    """Prueba que Pydantic bloquea un método de pago que no existe (ej: BITCOIN)"""
    
    json_invalido = {
        "numero_ticket": "T001-8888",
        "total": 150.00,
        "metodo_pago": "BITCOIN", # <-- Esto viola la regla de negocio
        "id_cajero": 1
    }
    
    respuesta = cliente_web.post('/api/tickets/', json=json_invalido)
    
    assert respuesta.status_code == 400

def test_crear_ticket_exito(cliente_web, mocker):
    """Prueba el flujo feliz (201 Created) usando un Mock para no tocar Supabase"""
    
    # MUY IMPORTANTE: Aunque probamos el Controlador, seguimos usando un Mock
    # para que la petición no guarde basura en la base de datos de producción.
    mocker.patch('src.controllers.ticket_controller.TicketVentaModel.crear_ticket', return_value=[{"id": 1}])
    
    json_perfecto = {
        "numero_ticket": "T001-8888",
        "total": 150.00,
        "metodo_pago": "EFECTIVO",
        "id_cajero": 1
    }
    
    respuesta = cliente_web.post('/api/tickets/', json=json_perfecto)
    
    # Verificaciones del éxito
    assert respuesta.status_code == 201
    datos_respuesta = respuesta.get_json()
    assert datos_respuesta["mensaje"] == "Ticket registrado con éxito"
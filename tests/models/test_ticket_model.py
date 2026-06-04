import pytest
from src.models.ticket_model import TicketVentaModel

# Datos falsos para inyectar en la prueba
DATOS_MOCK = {
    "numero_ticket": "T001-9999",
    "total": 15.50,
    "metodo_pago": "YAPE",
    "id_cajero": 1
}

def test_crear_ticket_exito(mocker):
    """Prueba que el modelo envía correctamente los datos a Supabase sin tocar la BD real"""
    
    # 1. Simular la respuesta de Supabase
    mock_supabase = mocker.patch('src.models.ticket_model.supabase.table')
    mock_supabase.return_value.insert.return_value.execute.return_value.data = [DATOS_MOCK]

    # 2. Ejecutar la función del modelo
    resultado = TicketVentaModel.crear_ticket(DATOS_MOCK)

    # 3. Verificaciones de seguridad
    assert isinstance(resultado, list)
    assert resultado[0]['numero_ticket'] == "T001-9999"
    # Verificar que el modelo apuntó a la tabla correcta
    mock_supabase.assert_called_with('tickets_venta')

def test_obtener_historial(mocker):
    """Prueba la extracción del historial con límite"""
    
    mock_supabase = mocker.patch('src.models.ticket_model.supabase.table')
    # Simulamos toda la cadena de métodos: select().order().limit().execute()
    mock_supabase.return_value.select.return_value.order.return_value.limit.return_value.execute.return_value.data = [DATOS_MOCK]

    resultado = TicketVentaModel.obtener_historial(limit=10)

    assert len(resultado) == 1
    assert resultado[0]['metodo_pago'] == "YAPE"
    mock_supabase.assert_called_with('tickets_venta')
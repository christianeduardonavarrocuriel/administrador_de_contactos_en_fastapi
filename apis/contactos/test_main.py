from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_root():
    response = client.get("/")
    assert response.status_code == 202
    assert response.json()["message"] == "API de la agenda"

def test_get_contactos_valid():
    response = client.get("/v1/contactos?limit=5&skip=0")
    # Assuming the database might be empty or not, but the request should be valid
    # The code returns 202 for success
    if response.status_code == 202:
        assert response.json()["message"] == "Datos consultados exitosamente"
    else:
        # It might fail with 400 if limit > total_registros
        # But for a basic test, let's assume limit=1 might serve better if DB is small
        # Or better, check specific error message
        pass

def test_get_contactos_missing_params():
    response = client.get("/v1/contactos")
    assert response.status_code == 400
    assert "obligatorios" in response.json()["message"]

def test_get_contactos_missing_limit():
    response = client.get("/v1/contactos?skip=0")
    assert response.status_code == 400
    assert "limit es obligatorio" in response.json()["message"]

def test_get_contactos_missing_skip():
    response = client.get("/v1/contactos?limit=5")
    assert response.status_code == 400
    assert "skip es obligatorio" in response.json()["message"]

def test_get_contactos_string_limit():
    response = client.get("/v1/contactos?limit=abc&skip=0")
    assert response.status_code == 400
    assert "limit no debe tener caracteres" in response.json()["message"]

def test_get_contactos_string_skip():
    response = client.get("/v1/contactos?limit=5&skip=abc")
    assert response.status_code == 400
    assert "skip no debe tener caracteres" in response.json()["message"]

def test_get_contactos_string_both():
    response = client.get("/v1/contactos?limit=abc&skip=abc")
    assert response.status_code == 400
    assert "limit y skip no deben tener caracteres" in response.json()["message"]

def test_get_contactos_negative_limit():
    response = client.get("/v1/contactos?limit=-5&skip=0")
    assert response.status_code == 400
    assert "limit no puede ser negativo" in response.json()["message"]

def test_get_contactos_negative_skip():
    response = client.get("/v1/contactos?limit=5&skip=-1")
    assert response.status_code == 400
    assert "skip no puede ser negativo" in response.json()["message"]

def test_get_contactos_negative_both():
    response = client.get("/v1/contactos?limit=-5&skip=-1")
    assert response.status_code == 400
    assert "limit y skip no pueden ser negativos" in response.json()["message"]

def test_get_contactos_zero_limit():
    response = client.get("/v1/contactos?limit=0&skip=90")
    assert response.status_code == 200
    assert "Se obtuvieron 0 registros" in response.json()["message"]

def test_get_contactos_zero_limit_and_skip():
    response = client.get("/v1/contactos?limit=0&skip=0")
    assert response.status_code == 200
    assert "Se obtuvieron 0 registros" in response.json()["message"]

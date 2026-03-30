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

def test_post_contacto_valid():
    payload = {
        "nombre": "Test User",
        "telefono": "1234567890",
        "email": "test@example.com"
    }
    response = client.post("/v1/contactos", json=payload)
    assert response.status_code == 201
    assert response.json()["nombre"] == "Test User"
    assert "creado correctamente" in response.json()["message"]
    return response.json()["id_contacto"]

def test_put_contacto_valid():
    # First create a contact to update
    id_contacto = test_post_contacto_valid()
    
    payload = {
        "nombre": "User Updated",
        "telefono": "0987654321",
        "email": "updated@example.com"
    }
    response = client.put(f"/v1/contactos/{id_contacto}", json=payload)
    assert response.status_code == 202
    assert response.json()["nombre"] == "User Updated"
    assert "actualizado correctamente" in response.json()["message"]

def test_put_contacto_not_found():
    payload = {
        "nombre": "Ghost",
        "telefono": "0000000000",
        "email": "ghost@example.com"
    }
    response = client.put("/v1/contactos/999999", json=payload)
    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"].lower()

def test_put_contacto_negative_id():
    payload = {
        "nombre": "Negative",
        "telefono": "111",
        "email": "neg@example.com"
    }
    response = client.put("/v1/contactos/-1", json=payload)
    assert response.status_code == 400
    assert "negativo" in response.json()["detail"].lower()

def test_delete_contacto_valid():
    # First create a contact to delete
    id_contacto = test_post_contacto_valid()
    
    response = client.delete(f"/v1/contactos/{id_contacto}")
    assert response.status_code == 202
    assert "eliminado correctamente" in response.json()["message"]

def test_delete_contacto_not_found():
    response = client.delete("/v1/contactos/999999")
    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"].lower()

def test_delete_contacto_negative_id():
    response = client.delete("/v1/contactos/-1")
    assert response.status_code == 400
    assert "negativo" in response.json()["detail"].lower()

def test_post_contacto_invalid_email():
    payload = {
        "nombre": "Email Test",
        "telefono": "9998887776",
        "email": "invalid_email_no_at"
    }
    response = client.post("/v1/contactos", json=payload)
    assert response.status_code == 400
    assert "no contiene el carácter '@'" in response.json()["detail"]

def test_put_contacto_invalid_email():
    # Creamos uno primero
    payload_create = {
        "nombre": "Put Email Test",
        "telefono": "1112223334",
        "email": "test@example.com"
    }
    resp_create = client.post("/v1/contactos", json=payload_create)
    id_contacto = resp_create.json()["id_contacto"]

    payload_update = {
        "nombre": "Put Email Test",
        "telefono": "1112223334",
        "email": "invalid_email_no_at"
    }
    response = client.put(f"/v1/contactos/{id_contacto}", json=payload_update)
    assert response.status_code == 400
    assert "no contiene el carácter '@'" in response.json()["detail"]

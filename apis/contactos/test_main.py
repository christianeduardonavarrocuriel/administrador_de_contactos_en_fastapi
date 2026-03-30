import requests
import pytest
import time


URL_BASE = "http://localhost:8000"


# TODO: 0. GET 202 / Mensaje de bienvenida
def test_read_root():
    url = f"{URL_BASE}/"
    response = requests.get(url)
    assert response.status_code == 202
    body = response.json()
    # Mensaje principal como en la implementación actual
    assert body["message"] == "API de la agenda"
    # Solo validamos que venga el campo de fecha/hora
    assert "datatime" in body


# TODO: 1. GET 202 /v1/contactos?limit=10&skip=0 primeros 10 contactos
def test_get_contactos_limit_10_skip_0():
    url = f"{URL_BASE}/v1/contactos?limit=10&skip=0"
    response = requests.get(url)
    assert response.status_code == 202
    data = response.json()
    assert data["message"] == "Datos consultados exitosamente"
    assert isinstance(data["items"], list)
    assert data["count"] == len(data["items"])


# TODO: 2. GET 202 /v1/contactos?limit=10&skip=90 ultimos 10 contacto
def test_get_contactos_limit_10_skip_90():
    url = f"{URL_BASE}/v1/contactos?limit=10&skip=90"
    response = requests.get(url)
    # Puede regresar 0 o más registros, pero debe ser exitoso
    assert response.status_code == 202
    data = response.json()
    assert data["message"] == "Datos consultados exitosamente"
    assert data["count"] == len(data["items"])


# TODO: 3. GET 400 /v1/contactos?limit=-10&skip=0 Error en limit
def test_get_contactos_limit_negativo_skip_0():
    url = f"{URL_BASE}/v1/contactos?limit=-10&skip=0"
    response = requests.get(url)
    assert response.status_code == 400
    assert "limit no puede ser negativo" in response.json()["message"]


# TODO: 4. GET 400 /v1/contactos?limit=10&skip=-10 Error en skip
def test_get_contactos_limit_10_skip_negativo():
    url = f"{URL_BASE}/v1/contactos?limit=10&skip=-10"
    response = requests.get(url)
    assert response.status_code == 400
    assert "skip no puede ser negativo" in response.json()["message"]


# TODO: 5. GET 202 /v1/contactos?limit=0&skip=0 vacio
def test_get_contactos_limit_0_skip_0():
    url = f"{URL_BASE}/v1/contactos?limit=0&skip=0"
    response = requests.get(url)
    assert response.status_code == 202
    assert "Se obtuvieron 0 registros" in response.json()["message"]


# TODO: 6. GET 202 /v1/contactos?skip=0 Regresar los primeros 10 contactos por default
def test_get_contactos_skip_0():
    url = f"{URL_BASE}/v1/contactos?skip=0"
    response = requests.get(url)
    assert response.status_code == 202
    data = response.json()
    assert isinstance(data["items"], list)
    assert data["limit"] == 10
    assert data["skip"] == 0
    assert data["count"] == 10
    assert len(data["items"]) == 10


# TODO: 7. GET 202 /v1/contactos?limit=10 Regresar los primeros 10 contactos por default
def test_get_contactos_limit_10():
    url = f"{URL_BASE}/v1/contactos?limit=10"
    response = requests.get(url)
    assert response.status_code == 202
    data = response.json()
    assert isinstance(data["items"], list)
    assert data["limit"] == 10
    assert data["skip"] == 0
    assert data["count"] == 10
    assert len(data["items"]) == 10


# TODO: 8. GET 202 /v1/contactos Regresar los primeros 10 contactos por default
def test_get_contactos():
    url = f"{URL_BASE}/v1/contactos"
    response = requests.get(url)
    assert response.status_code == 202
    data = response.json()
    assert isinstance(data["items"], list)
    assert data["limit"] == 10
    assert data["skip"] == 0
    assert data["count"] == 10
    assert len(data["items"]) == 10


# TODO: 9. GET 400 /v1/contactos?limit=x&skip=100 Mensaje de Error en limit
def test_get_contactos_limit_x_skip_100():
    url = f"{URL_BASE}/v1/contactos?limit=x&skip=100"
    response = requests.get(url)
    assert response.status_code == 400
    assert "limit no debe tener caracteres" in response.json()["message"]
    
# TODO: 10. GET 400 /v1/contactos?limit=10&skip=x Mensaje de Error en skip
def test_get_contactos_limit_10_skip_x():
    url = f"{URL_BASE}/v1/contactos?limit=10&skip=x"
    response = requests.get(url)
    assert response.status_code == 400
    assert "skip no debe tener caracteres" in response.json()["message"]

# TODO: 11. POST 201 /v1/contactos Insertar un nuevo contacto (Exitoso)
def test_create_contacto_success():
    url = f"{URL_BASE}/v1/contactos"
    # Este test asume que el teléfono no existe inicialmente o se limpia la DB
    payload = {
        "nombre": "Test Cliente",
        "telefono": "1234567890",
        "email": "test_cliente@example.com"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Test Cliente"
    assert "id_contacto" in data


# TODO: 12 POST 400 /v1/contactos Error teléfono duplicado
def test_create_contacto_error_duplicate():
    url = f"{URL_BASE}/v1/contactos"
    payload = {
        "nombre": "Test Duplicado",
        "telefono": "1234567890",
        "email": "duplicado@example.com"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert "Ya existe un contacto con ese teléfono" in response.json()["detail"]


# TODO: 13. GET 202 /v1/contactos/{id_contacto} Consultar un contacto por ID
def test_get_contacto_id():
    id_contacto = 1 # Usamos un ID fijo que sepamos que existe
    url = f"{URL_BASE}/v1/contactos/{id_contacto}"
    response = requests.get(url)
    assert response.status_code == 202


# TODO: 14. PUT 202 /v1/contactos/{id_contacto} Actualizar un contacto
def test_update_contacto():
    id_contacto = 1
    url = f"{URL_BASE}/v1/contactos/{id_contacto}"
    payload = {
        "nombre": "Cliente Actualizado",
        "telefono": "0987654321",
        "email": "actualizado@example.com"
    }
    response = requests.put(url, json=payload)
    assert response.status_code in [202, 404]


# TODO: 15. DELETE 202 /v1/contactos/{id_contacto} Borrar un contacto
def test_delete_contacto():
    # En pruebas con datos fijos, a veces es mejor borrar uno que acabamos de crear
    # o simplemente intentar borrar uno alto para no vaciar la tabla de base
    url = f"{URL_BASE}/v1/contactos/999" 
    response = requests.delete(url)
    assert response.status_code in [202, 404]


# TODO: 16. POST 400 /v1/contactos Error email sin @
def test_create_contacto_error_email():
    url = f"{URL_BASE}/v1/contactos"
    payload = {
        "nombre": "Error Email",
        "telefono": "0000000000",
        "email": "email_sin_arroba"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert "email no contiene el carácter '@'" in response.json()["detail"]


# TODO: 16. PUT 400 /v1/contactos/{id_contacto} Error email sin @ en actualizar
def test_update_contacto_error_email():
    url = f"{URL_BASE}/v1/contactos/1"
    payload = {
        "nombre": "Error Email Upd",
        "telefono": "1111111111",
        "email": "email_sin_arroba_upd"
    }
    response = requests.put(url, json=payload)
    assert response.status_code == 400
    assert "email no contiene el carácter '@'" in response.json()["detail"]


# TODO: 18. GET 400 /v1/contactos/{id_contacto} Error ID negativo
def test_get_contacto_id_negativo():
    url = f"{URL_BASE}/v1/contactos/-5"
    response = requests.get(url)
    assert response.status_code == 400
    assert "número negativo" in response.json()["message"]
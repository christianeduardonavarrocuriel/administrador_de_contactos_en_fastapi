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
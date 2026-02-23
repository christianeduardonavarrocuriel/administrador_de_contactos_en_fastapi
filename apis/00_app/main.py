"""Aplicación de ejemplo con FastAPI.

Este módulo expone una API muy sencilla para:
- Probar que el servidor FastAPI se levanta correctamente.
- Devolver un saludo básico en la raíz.
- Regresar una lista estática de clientes de prueba.
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_root():
    """Endpoint raíz de prueba.

    Retorna un JSON sencillo para validar que la API está funcionando.
    """
    return {"Hello": "World"}

@app.get("/clientes")
def get_clientes():
    """Obtiene una lista de clientes de ejemplo.

    Devuelve una lista estática con nombres, útil para pruebas rápidas.
    """
    data = [
        {
            "nombre":"Dejah"
        },
        {
            "nombre":"John"
        }
    ]
    return data

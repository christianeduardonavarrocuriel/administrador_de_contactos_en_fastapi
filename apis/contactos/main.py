from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import sqlite3 as sqlite

app = FastAPI()

@app.get("/",
 status_code=202,
 summary="Endpoint raíz",
 description= "Bienvenido a la API de agenda")
def get_root():
    response = {
        "message": "API de la agenda",
        "datatime": "12/02/2026"
        }
    return response

@app.get(
    "/v1/contactos",
    status_code=202,
    summary="Endpoint que ingresa los contactos paginados",
    description= """Endpoint que ingresa los contactos paginados,
    utiliza los siguientes query params:
    limit:int -> Indica el número de registros a regresar
    skip:int -> Indica el número de registros a omitir"""
)
async def get_contactos(limit: int = 10, skip: int = 0):
  #  TODO: Conectar con la base de datos agenda.db
  #  TODO: Consultar los registros de la tabla contactos
  #  TODO: Formatear la respuesta con el siguiente schema:
  #  TODO: Responder la petición

    try:
        db = sqlite.connect("agenda.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM contactoss LIMIT ? OFFSET ?", (limit, skip))
        contactos = cursor.fetchall()
        print(contactos)

        data = {
            "table": "contactos",
            "items": [
                {
                    "id_contacto":1,
                    "nombre":"Dejah",
                    "telefono":"1234567890",
                    "email":"dejah@email.com"
                },
                {
                    "id_contacto":2,
                    "nombre":"John Carter",
                    "telefono":"0987654321",
                    "email":"john@email.com"    
                },
            ],
            "count": 2,
            "datetime": "12/02/2026 10:28:30",
            "message": "Datos consultados exitosamente",
            "limit":limit,
            "skip":skip
        }
        return JSONResponse(
            status_code=202,
            content=data
        )
    except Exception as e:
        print(f"Error al consultar la base de datos: {e.args}")
        #raise HTTPException(status_code=400, detail="Error al consultar los datos")
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": "12/02/2026 10:28:30",
                "message": "Error al consultar los datos",
                "limit":limit,
                "skip":skip
                }
            )
"""API de contactos con FastAPI.

Este módulo expone una API REST para gestionar una agenda de contactos
almacenados en una base de datos SQLite (`agenda.db`). Incluye endpoints
para consultar contactos con paginación, obtener un contacto por ID y
crear nuevos registros con validaciones.
"""

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3 as sqlite
from typing import Optional
from datetime import datetime

app = FastAPI()


class ContactoIn(BaseModel):
    nombre: str
    telefono: str
    email: str

@app.get("/",
 status_code=202,
 summary="Endpoint raíz",
 description= "Bienvenido a la API de agenda")
def get_root():
    """Endpoint raíz de la API de contactos.

    Devuelve un mensaje de bienvenida y la fecha/hora actual formateada.
    """
    response = {
        "message": "API de la agenda",
        "datatime": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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
async def get_contactos(
    limit: Optional[str] = Query(default=None),
    skip: Optional[str] = Query(default=None),
):
    """Obtiene contactos paginados desde la base de datos.

    - `limit`: número máximo de registros a devolver.
    - `skip`: número de registros a omitir desde el inicio.

    Aplica validaciones sobre los parámetros y devuelve mensajes de error
    claros cuando los valores son inválidos.
    """

    # Validación si limit o skip tienen caracteres
    limit_error = False
    skip_error = False

    try:
        if limit is not None:
            int(limit)
    except ValueError:
        limit_error = True

    try:
        if skip is not None:
            int(skip)
    except ValueError:
        skip_error = True

    if limit_error and skip_error:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error: los parámetros limit y skip no deben tener caracteres",
                "limit": limit,
                "skip": skip,
            },
        )
    elif limit_error:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error: el parámetro limit no debe tener caracteres",
                "limit": limit,
                "skip": skip,
            },
        )
    elif skip_error:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error: el parámetro skip no debe tener caracteres",
                "limit": limit,
                "skip": skip,
            },
        )

    # Conversión a enteros
    if limit is not None:
        limit = int(limit)
    if skip is not None:
        skip = int(skip)

    # Validación de parámetros vacíos
    if limit is None and skip is None:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error: los parámetros limit y skip son obligatorios",
                "limit": limit,
                "skip": skip,
            },
        )

    if limit is None:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error: el parámetro limit es obligatorio",
                "limit": limit,
                "skip": skip,
            },
        )

    if skip is None:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error: el parámetro skip es obligatorio",
                "limit": limit,
                "skip": skip,
            },
        )

    # Validación de parámetros: limit y skip no pueden ser negativos
    if limit < 0 and skip < 0:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error: los parámetros limit y skip no pueden ser negativos",
                "limit": limit,
                "skip": skip,
            },
        )

    if limit < 0:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error: el parámetro limit no puede ser negativo",
                "limit": limit,
                "skip": skip,
            },
        )

    if skip < 0:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error: el parámetro skip no puede ser negativo",
                "limit": limit,
                "skip": skip,
            },
        )

    if limit == 0:
        return JSONResponse(
            status_code=200,
            content={
                "table": "contactos",
                "items": [],
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Se obtuvieron 0 registros",
                "limit": limit,
                "skip": skip,
            },
        )

    try:
        db = sqlite.connect("agenda.db")
        cursor = db.cursor()

        # Validar que el rango de limit no exceda el total de registros
        cursor.execute("SELECT COUNT(*) FROM contactos")
        total_registros = cursor.fetchone()[0]

        if limit > total_registros and total_registros > 0:
            return JSONResponse(
                status_code=400,
                content={
                    "table": "contactos",
                    "items": [],
                    "count": 0,
                    "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "message": "Error: el parámetro limit excede el número de registros disponibles",
                    "limit": limit,
                    "skip": skip,
                },
            )

        cursor.execute("SELECT * FROM contactos LIMIT ? OFFSET ?", (limit, skip))
        contactos = cursor.fetchall()
        items = [
            {
                "id_contacto": row[0],
                "nombre": row[1],
                "telefono": row[2],
                "email": row[3],
            }
            for row in contactos
        ]

        data = {
            "table": "contactos",
            "items": items,
            "count": len(items),
            "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "message": "Datos consultados exitosamente",
            "limit": limit,
            "skip": skip,
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
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error al consultar los datos",
                "limit":limit,
                "skip":skip
                }
            )


@app.get(
    "/v1/contactos/{id_contacto}",
    status_code=202,
    summary="Consultar un contacto por ID",
    description="Busca un contacto específico en la tabla contactos usando id_contacto",
)
async def get_contacto_por_id(id_contacto: int):
    """Obtiene un contacto específico por su identificador.

    Si `id_contacto` es negativo o el registro no existe, devuelve una
    respuesta JSON con el mensaje de error correspondiente.
    """
    # Validación: id_contacto no puede ser negativo
    if id_contacto < 0:
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error: No puedes ingresas un número negativo en id_contacto",
            },
        )

    try:
        db = sqlite.connect("agenda.db")
        cursor = db.cursor()
        cursor.execute(
            "SELECT id_contacto, nombre, telefono, email FROM contactos WHERE id_contacto = ?",
            (id_contacto,),
        )
        row = cursor.fetchone()

        if row is None:
            # Contacto no encontrado
            return JSONResponse(
                status_code=400,
                content={
                    "table": "contactos",
                    "item": {},
                    "count": 0,
                    "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "message": "Contacto no encontrado",
                },
            )

        item = {
            "id_contacto": row[0],
            "nombre": row[1],
            "telefono": row[2],
            "email": row[3],
        }

        data = {
            "table": "contactos",
            "items": item,
            "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "message": "Datos consultados exitosamente",
        }
        return JSONResponse(status_code=202, content=data)
    except Exception as e:
        print(f"Error al consultar el contacto por id: {e.args}")
        return JSONResponse(
            status_code=400,
            content={
                "table": "contactos",
                "item": {},
                "count": 0,
                "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": "Error al Buscar el Registro",
            },
        )
    finally:
        try:
            db.close()
        except Exception:
            pass


@app.post(
    "/v1/contactos",
    status_code=201,
    summary="Crear un nuevo contacto",
    description="Inserta un nuevo contacto en la tabla contactos de la agenda",
)
async def create_contacto(contacto: ContactoIn):
    """Crea un nuevo contacto en la agenda.

    Valida que los campos no vengan vacíos, que no contengan solo
    espacios y que no utilicen el valor por defecto "string". También
    maneja errores de integridad (teléfono duplicado) y errores
    generales de base de datos.
    """
    # Validación de campos vacíos o solo espacios
    campos_vacios = []
    if not contacto.nombre.strip():
        campos_vacios.append("nombre")
    if not contacto.telefono.strip():
        campos_vacios.append("telefono")
    if not contacto.email.strip():
        campos_vacios.append("email")

    # Validación de valores por defecto "string"
    campos_string = []
    if contacto.nombre.strip().lower() == "string":
        campos_string.append("nombre")
    if contacto.telefono.strip().lower() == "string":
        campos_string.append("telefono")
    if contacto.email.strip().lower() == "string":
        campos_string.append("email")

    # Construir mensaje según los casos presentes
    if campos_vacios or campos_string:
        partes_mensaje = []
        if campos_vacios:
            partes_mensaje.append(
                f"Datos en {', '.join(campos_vacios)} no introducidos"
            )
        if campos_string:
            partes_mensaje.append(
                f"palabra string escrita en {', '.join(campos_string)}"
            )

        detalle = "Error: " + " y ".join(partes_mensaje)
        raise HTTPException(
            status_code=400,
            detail=detalle,
        )

    try:
        db = sqlite.connect("agenda.db")
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO contactos (nombre, telefono, email) VALUES (?, ?, ?)",
            (contacto.nombre, contacto.telefono, contacto.email),
        )
        db.commit()
        new_id = cursor.lastrowid

        data = {
            "id_contacto": new_id,
            "nombre": contacto.nombre,
            "telefono": contacto.telefono,
            "email": contacto.email,
            "message": "Contacto creado correctamente",
        }
        return JSONResponse(status_code=201, content=data)
    except sqlite.IntegrityError:
        # Por ejemplo, si el teléfono ya existe (campo UNIQUE)
        raise HTTPException(
            status_code=400,
            detail="Ya existe un contacto con ese teléfono",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al insertar el contacto en la base de datos",
        )
    finally:
        try:
            db.close()
        except Exception:
            pass
# apis_demo

## Descripción

Este proyecto es una **API REST de agenda de contactos** construida con **Python**, **FastAPI** y **SQLite**. Expone endpoints para consultar contactos (con paginación), obtener un contacto por ID y crear nuevos registros con validaciones, enfocándose en buenas prácticas de diseño de APIs y acceso a base de datos.

Se cubren aspectos como:
- Modelado básico de datos para una agenda de contactos.
- Paginación con parámetros `limit` y `skip`.
- Manejo explícito de errores y mensajes claros al cliente.
- Uso de consultas parametrizadas para prevenir inyección SQL.

## Tecnologías

- **Lenguaje:** Python
- **Framework web:** FastAPI
- **Ejecución local:** CLI de FastAPI (`fastapi dev`)
- **Base de datos:** SQLite (`agenda.db`)
- **Validación de datos:** Pydantic (modelos `BaseModel`)
- **Cliente para pruebas:** curl o cualquier cliente HTTP (Insomnia, Postman, etc.)

## Instalación y ejecución

1. Clonar el repositorio:
    ```bash
    git clone https://github.com/christianeduardonavarrocuriel/apis_demo.git
    cd apis_demo
    ```

2. Crear y activar un entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # .venv\Scripts\activate  # Windows PowerShell
    ```

3. Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```

4. Crear la base de datos SQLite (si aún no existe) desde `apis/contactos/agenda.sql` o usando el script SQL del README.

5. Levantar los servidores de desarrollo con la CLI de FastAPI:

    Desde la raíz del proyecto:

    ```bash
    source .venv/bin/activate          # activar entorno virtual (Linux/macOS)
    cd apis

    # API de ejemplo
    fastapi dev 00_app/main.py

    # API de contactos
    fastapi dev contactos/main.py
    ```

    Por defecto la API que se esté ejecutando quedará disponible en:
    - Documentación interactiva: http://127.0.0.1:8000/docs
    - Redoc: http://127.0.0.1:8000/redoc

## Endpoints principales

Los endpoints principales del módulo de contactos son:

- `GET /` — Endpoint raíz de la API de contactos.
- `GET /v1/contactos` — Consultar todos los contactos (paginados con `limit` y `skip`).
- `GET /v1/contactos/{id_contacto}` — Consultar un contacto específico por ID.
- `POST /v1/contactos` — Crear un nuevo contacto.

La especificación detallada de cada endpoint (campos, códigos de respuesta, ejemplos de errores, etc.) se encuentra en las tablas de las secciones posteriores de este README.

1. Esquema de datos (tabla contactos)

|  Contactos    |              | 
|:-------------:|:------------:|
| id_contacto   | int PK       |
| nombre        | varchar (100)|
|email          | varchar (100)|
|telefono       | varchar (100)|

2. Consultar Todos los Contactos

|No.|Propiedad|Detalle|
|:-:|:------:|:------:|
|1|Descripción|Endpoint para consultar todos los contactos de forma paginada.|
|2|Summary|Devuelve la lista de contactos paginados.|
|3|Method|GET|
|4|Endpoint|/v1/contactos|
|5|Authentication|NA|
|6|Query Param|limit:int & skip:int (obligatorios, valores >= 0)|
|7|Path Param|NA|
|8|Data|NA|
|9|Status Code|202|
|10|Response|{"table": "contactos", "items": [{"id_contacto": int, "nombre": str, "email": str, "telefono": str }], "count": int, "datetime": timestamp, "message": "Datos consultados exitosamente", "limit": int, "skip": int}|
|11|Response Type|application/json|
|12|Status Code (error)|400|
|13|Response Type (error)|application/json|
|14|Response (error)|{"table":"contactos","items":[],"count":0,"datetime":"timestamp","message":"Error: los parámetros limit y skip son obligatorios"} / {"message":"Error: el parámetro limit es obligatorio"} / {"message":"Error: el parámetro skip es obligatorio"} / {"message":"Error: el parámetro limit no puede ser negativo"} / {"message":"Error: el parámetro skip no puede ser negativo"} / {"message":"Error: los parámetros limit y skip no pueden ser negativos"} / {"message":"Error: el parámetro limit excede el número de registros disponibles"} / {"message":"Error al consultar los datos"}|
|15|cURL|curl -X GET "http://127.0.0.1:8000/v1/contactos?limit=10&skip=0"|  

|No.|Propiedad|Detalle|
|:-:|:------:|:---:|
|1|Descripción|Endpoint para consultar un contacto por su identificador único.|
|2|Summary|Devuelve un contacto específico por ID.|
|3|Version|V1|
|4|Method|GET|
|5|Endpoint|/v1/contactos/{id_contacto}|
|6|Query Param|NA|
|7|Path Param|id_contacto:int|
|8|Data|NA|
|9|Status Code|202|
|10|Response Type|application/json|
|11|Response|{"table":"contactos", "items": {"id_contacto":int, "nombre": str,"email": str, "telefono": str},"datetime": timestamp, "message":"Datos consultados exitosamente"}|
|11.5|Response (error)|{"table": "contactos","item": {},"count": 0, "datetime": timestamp, "message": "Contacto no encontrado"} / {"message": "Error: No puedes ingresas un número negativo en id_contacto"}|
|12|Status Code (error)|400|
|13|Response Type (error)|application/json|
|14|Response (error)|{"table":"contactos","item":{},"count":0,"datetime":"timestamp","message":"Error al Buscar el Registro"}|
|15|cURL|curl -X GET http://localhost:8000/v1/contactos/3|

3. Crear un nuevo contacto

|No.|Propiedad|Detalle|
|:-:|:------:|:------:|
|1|Descripción|Endpoint para registrar un nuevo contacto en la agenda.|
|2|Summary|Inserta un nuevo registro en la tabla contactos.|
|3|Method|POST|
|4|Endpoint|/v1/contactos|
|5|Authentication|NA|
|6|Query Param|NA|
|7|Path Param|NA|
|8|Data|Body (JSON): {"nombre": str, "telefono": str, "email": str}|
|9|Status Code|201|
|10|Response|{"id_contacto": int, "nombre": str, "telefono": str, "email": str, "message": "Contacto creado correctamente"}|
|11|Response Type|application/json|
|12|Reglas de validación|Todos los campos son obligatorios, no pueden venir vacíos ni contener solo espacios y no pueden tener el valor "string" (sin importar mayúsculas/minúsculas).|
|13|Status Code (error)|400, 500|
|14|Response (error) 400|{"detail": "Error: Datos en [campos_vacios] no introducidos"}, {"detail": "Error: palabra string escrita en [campos_string]"}, o combinación: {"detail": "Error: Datos en [campos_vacios] no introducidos y palabra string escrita en [campos_string]"}|
|15|Response (error) 500|{"detail": "Error al insertar el contacto en la base de datos"}|
|16|Ejemplo Body|{"nombre": "Juan Pérez", "telefono": "5551234567", "email": "juan.perez@example.com"}|
|17|cURL|curl -X POST http://127.0.0.1:8000/v1/contactos -H "Content-Type: application/json" -d '{"nombre": "Juan Pérez", "telefono": "5551234567", "email": "juan.perez@example.com"}'|

# API Contactos

API REST para la gestión de una agenda de contactos, construida con **FastAPI** y **SQLite**.

---

> A continuación se mostrarán tabs para:
> `[BASE DE DATOS]` · `[IMPORTAR DATOS]` · `[MODELO]` · `[ENDPOINT RAÍZ]` · `[GET TODOS]` · `[GET POR ID]` · `[POST]` · `[VALIDACIONES]` · `[ERRORES]` · `[SEGURIDAD]`

---

## `[BASE DE DATOS]` — Esquema de la Tabla

La base de datos SQLite se llama `agenda.db` y se genera en el directorio desde donde se ejecuta el servidor.  
El script DDL se encuentra en `agenda.sql`.

```sql
CREATE TABLE contactos (
    id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      VARCHAR(255) NOT NULL,
    telefono    VARCHAR(20)  NOT NULL UNIQUE,
    email       VARCHAR(255) NOT NULL
);
```

| Campo | Tipo | Restricciones |
|:-----:|:----:|:-------------:|
| `id_contacto` | INTEGER | PK, AUTOINCREMENT |
| `nombre` | VARCHAR(255) | NOT NULL |
| `telefono` | VARCHAR(20) | NOT NULL, UNIQUE |
| `email` | VARCHAR(255) | NOT NULL |

---

## `[IMPORTAR DATOS]` — Cargar datos desde CSV

Para poblar la base de datos usando el archivo `data.csv`:

```bash
sqlite3 agenda.db
```

```sql
.mode csv
.import data.csv contactos
SELECT * FROM contactos;
```

> **Nota:** El campo `telefono` tiene restricción `UNIQUE`, por lo que no se puede importar un CSV con teléfonos duplicados.

---

## `[MODELO]` — Modelo de Entrada (Pydantic)

El endpoint `POST /v1/contactos` recibe el siguiente body validado por Pydantic:

```python
class ContactoIn(BaseModel):
    nombre: str
    telefono: str
    email: str
```

Todos los campos son obligatorios. No pueden estar vacíos, contener solo espacios ni tener el valor literal `"string"`.

---

## `[ENDPOINT RAÍZ]` — GET /

| No. | Propiedad | Detalle |
|:---:|:---------:|:-------:|
| 1 | Descripción | Bienvenida a la API de agenda |
| 2 | Summary | Endpoint raíz |
| 3 | Method | GET |
| 4 | Endpoint | `/` |
| 5 | Authentication | NA |
| 6 | Query Param | NA |
| 7 | Path Param | NA |
| 8 | Data | NA |
| 9 | Status Code | 202 |
| 10 | Response | `{"message": "API de la agenda", "datetime": "dd/mm/yyyy HH:MM:SS"}` |
| 11 | Response Type | application/json |
| 12 | cURL | `curl -X GET http://127.0.0.1:8000/` |

---

## `[GET TODOS]` — GET /v1/contactos — Consultar Todos los Contactos (Paginados)

Esta sección hace referencia a la tabla **"2. Consultar Todos los Contactos"** al inicio del documento, donde se describen todas las propiedades del endpoint.

- Endpoint: `GET /v1/contactos`
- Descripción: Consultar todos los contactos paginados.
- Ver validaciones específicas en la sección `[VALIDACIONES]` (GET /v1/contactos).
- Ver catálogo completo de errores en la sección `[ERRORES]` (GET /v1/contactos — 400).

Ejemplo de respuesta exitosa:

```json
{
    "table": "contactos",
    "items": [
        {"id_contacto": 1, "nombre": "Juan Pérez", "email": "juan.perez@example.com", "telefono": "5551234567"}
    ],
    "count": 1,
    "datetime": "timestamp",
    "message": "Datos consultados exitosamente",
    "limit": 10,
    "skip": 0
}
```

---

## `[GET POR ID]` — GET /v1/contactos/{id_contacto} — Consultar un Contacto por ID

Esta sección hace referencia a la tabla **"Consultar un contacto por su ID"** al inicio del documento, donde se describen todas las propiedades del endpoint.

- Endpoint: `GET /v1/contactos/{id_contacto}`
- Descripción: Consultar un contacto específico por su identificador.
- Ver validaciones específicas en la sección `[VALIDACIONES]` (GET /v1/contactos/{id_contacto}).
- Ver catálogo completo de errores en la sección `[ERRORES]` (GET /v1/contactos/{id_contacto} — 400).

Ejemplo de respuesta exitosa:

```json
{
    "table": "contactos",
    "items": {"id_contacto": 3, "nombre": "María López", "email": "maria.lopez@example.com", "telefono": "5559876543"},
    "datetime": "timestamp",
    "message": "Datos consultados exitosamente"
}
```

---

## `[POST]` — POST /v1/contactos — Crear un Nuevo Contacto

Esta sección hace referencia a la tabla **"3. Crear un nuevo contacto"** al inicio del documento, donde se describen todas las propiedades del endpoint.

- Endpoint: `POST /v1/contactos`
- Descripción: Crear un nuevo contacto en la agenda.
- Ver reglas de validación en la sección `[VALIDACIONES]` (POST /v1/contactos).
- Ver catálogo completo de errores en la sección `[ERRORES]` (POST /v1/contactos — 400 / 500).

Ejemplo de body de petición:

```json
{
    "nombre": "Juan Pérez",
    "telefono": "5551234567",
    "email": "juan.perez@example.com"
}
```

Ejemplo de respuesta exitosa:

```json
{
    "id_contacto": 10,
    "nombre": "Juan Pérez",
    "telefono": "5551234567",
    "email": "juan.perez@example.com",
    "message": "Contacto creado correctamente"
}
```

---

## `[VALIDACIONES]` — Reglas de Validación por Endpoint

### GET /v1/contactos — Paginación

| Condición | Mensaje de Error |
|:---------:|:----------------:|
| `limit` y `skip` ausentes | `"Error: los parámetros limit y skip son obligatorios"` |
| Solo `limit` ausente | `"Error: el parámetro limit es obligatorio"` |
| Solo `skip` ausente | `"Error: el parámetro skip es obligatorio"` |
| `limit < 0` y `skip < 0` | `"Error: los parámetros limit y skip no pueden ser negativos"` |
| `limit < 0` | `"Error: el parámetro limit no puede ser negativo"` |
| `skip < 0` | `"Error: el parámetro skip no puede ser negativo"` |
| `limit > total_registros` | `"Error: el parámetro limit excede el número de registros disponibles"` |

### GET /v1/contactos/{id_contacto}

| Condición | Mensaje de Error |
|:---------:|:----------------:|
| `id_contacto < 0` | `"Error: No puedes ingresas un número negativo en id_contacto"` |
| Registro no encontrado | `"Contacto no encontrado"` |

### POST /v1/contactos

| Condición | Mensaje de Error |
|:---------:|:----------------:|
| Campo vacío o solo espacios | `"Error: Datos en [campo] no introducidos"` |
| Campo con valor `"string"` | `"Error: palabra string escrita en [campo]"` |
| Teléfono duplicado (UNIQUE) | `"Ya existe un contacto con ese teléfono"` |

---

## `[ERRORES]` — Catálogo Completo de Respuestas de Error

### GET /v1/contactos — 400

```json
{
    "table":"contactos",
    "items":[],
    "count":0,
    "datetime":"timestamp",
    "message":"Error: los parámetros limit y skip son obligatorios",
    "limit":null,
    "skip":null
}

{
    "table":"contactos",
    "items":[],
    "count":0,
    "datetime":"timestamp",
    "message":"Error: el parámetro limit es obligatorio",
    "limit":null,
    "skip":0
}

{
    "table":"contactos",
    "items":[],
    "count":0,
    "datetime":"timestamp",
    "message":"Error: el parámetro skip es obligatorio",
    "limit":10,
    "skip":null
}

{
    "table":"contactos",
    "items":[],
    "count":0,
    "datetime":"timestamp",
    "message":"Error: el parámetro limit no puede ser negativo",
    "limit":-1,
    "skip":0
}

{
    "table":"contactos",
    "items":[],
    "count":0,
    "datetime":"timestamp",
    "message":"Error: el parámetro skip no puede ser negativo",
    "limit":10,
    "skip":-1
}

{
    "table":"contactos",
    "items":[],
    "count":0,
    "datetime":"timestamp",
    "message":"Error: los parámetros limit y skip no pueden ser negativos",
    "limit":-1,
    "skip":-1
}

{
    "table":"contactos",
    "items":[],
    "count":0,
    "datetime":"timestamp",
    "message":"Error: el parámetro limit excede el número de registros disponibles",
    "limit":999,
    "skip":0
}

{
    "table":"contactos",
    "items":[],
    "count":0,
    "datetime":"timestamp",
    "message":"Error al consultar los datos",
    "limit":10,
    "skip":0
}
```

### GET /v1/contactos/{id_contacto} — 400

```json
{
    "table":"contactos",
    "item":{},
    "count":0,
    "datetime":"timestamp",
    "message":"Error: No puedes ingresas un número negativo en id_contacto"
}

{
    "table":"contactos",
    "item":{},
    "count":0,
    "datetime":"timestamp",
    "message":"Contacto no encontrado"
}

{
    "table":"contactos",
    "item":{},
    "count":0,
    "datetime":"timestamp",
    "message":"Error al Buscar el Registro"
}
```

### POST /v1/contactos — 400 / 500

```json
{
    "detail": "Error: Datos en nombre no introducidos"
}

{
    "detail": "Error: Datos en telefono, email no introducidos"
}

{
    "detail": "Error: palabra string escrita en nombre"
}

{
    "detail": "Error: Datos en telefono no introducidos y palabra string escrita en nombre"
}

{
    "detail": "Ya existe un contacto con ese teléfono"
}

{
    "detail": "Error al insertar el contacto en la base de datos"
}
```

---

## `[SEGURIDAD]` — Buenas Prácticas Implementadas

| Práctica | Descripción |
|:--------:|:-----------:|
| Consultas parametrizadas (`?`) | Previene inyección SQL al no concatenar valores directamente en las queries |
| Validación con Pydantic | El modelo `ContactoIn` valida tipos antes de llegar a la base de datos |
| Validación explícita de campos | Se rechazan valores vacíos y el placeholder `"string"` de Swagger UI |
| Bloque `finally` | Cierra la conexión a la base de datos en todos los casos (éxito o error) |
| `try/except` en todos los endpoints | Evita exponer trazas internas; retorna mensajes de error controlados |

```python
# Ejemplo de consulta parametrizada — previene SQL Injection
cursor.execute(
    "SELECT * FROM contactos LIMIT ? OFFSET ?",
    (limit, skip)
)
```

## Autor

- **Autor:** Christian Eduardo Navarro Curiel
- **GitHub:** https://github.com/christianeduardonavarrocuriel

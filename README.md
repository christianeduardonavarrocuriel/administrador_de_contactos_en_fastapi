# apis_demo

|  Contactos    |              | 
|:-------------:|:------------:|
| id_contacto   | int PK       |
| nombre        | varchar (100)|
|email          | varchar (100)|
|telefono       | varchar (100)|

2. Consultar Todos los Contactos

|No.|Propiedad|Detalle|
|:-:|:------:|:------:|
|1|Descripción|Endpoint para Consultar todos los Contactos|
|2|Summary|Regresa los Contactos Paginados|
|3|Method|GET|
|4|Endpoint|/v1/contactos/|
|5|Authentication|NA|
|6|Query Param|limit:int&skip:int|
|7|Path Param|NA|
|8|Data|NA|
|9|Status Code|202|
|10|Response|Indicación de lo que mandará la respuesta de esa consulta. Por Ejemplo: {"table": "contactos", "items": [ {"id_contacto": int, "nombre": str, "email": str, "telefono": str }, ] "count": int, "datetime": timestamp, "message": "Datos Consultados Exitosamente" }|
|11|Responsive Type|application/json|
|12|Status Code (error)|400, 401, 403, 404, 409, 422, 500, 501, 502, 503, 504|
|13|Responsive Type (error)|NA|
|14|Response (error)|{"detail":"Parámetros inválidos", "datetime":"timestamp"} / {"detail":"Token inválido o no proporcionado", "datetime":"timestamp"} / {"detail":"Acceso prohibido", "datetime":"timestamp"} / {"detail":"No se encontraron contactos", "datetime":"timestamp"} / {"detail":"Conflicto: contacto duplicado", "datetime":"timestamp"} / {"detail":"Error de validación", "datetime":"timestamp"} / {"detail":"Error interno al consultar contactos", "datetime":"timestamp"} / {"detail":"Error de comunicación con servidor externo", "datetime":"timestamp"} / {"detail":"Servicio no disponible", "datetime":"timestamp"} / {"detail":"Tiempo de espera agotado", "datetime":"timestamp"}|
|15|cURL|curl -X GET http://127.0.0.1:8000/|  

|No.|Propiedad|Detalle|
|:-:|:------:|:---:|
|1|Description|
|2|Summary|
|3|Version|V1|
|4|Method|GET|
|5|Endpoint|/v1/contactos/{id_contacto}|
|6|Query Param|NA|
|7|Path Param|id_contacto|
|8|Data|NA|
|9|Status Code|202|
|10|Response Type|application/json|
|11|Response|{"table":"contactos", "items": {"id_contacto":int, "nombre": str,"email": str, "telefono": str},"datetime": timestamp, "message":"Datos consultados exitosamente"}|
|11.5| Response (error)|{"table": "contactos","item": {},"count": 0, "datetime": timestamp, "message": "Contacto no encontrado"}|
|12|Status Code (error)|400|
|13|Response Type (error)|applicaction/json|
|14|Response (error)|{"error": "Error al Buscar el Registro"}|
|15|cURL|curl -X GET http://localhost:8000/v1/contactos/3|

3. Crear un nuevo contacto

|No.|Propiedad|Detalle|
|:-:|:------:|:------:|
|1|Descripción|Endpoint para crear un nuevo contacto en la agenda|
|2|Summary|Inserta un registro en la tabla contactos|
|3|Method|POST|
|4|Endpoint|/v1/contactos|
|5|Authentication|NA|
|6|Query Param|NA|
|7|Path Param|NA|
|8|Data|Body (JSON): {"nombre": str, "telefono": str, "email": str}|
|9|Status Code|201|
|10|Response|{"id_contacto": int, "nombre": str, "telefono": str, "email": str, "message": "Contacto creado correctamente"}|
|11|Response Type|application/json|
|12|Reglas de validación|Todos los campos son obligatorios y no pueden venir vacíos ni solo con espacios. Ningún campo puede tener el valor "string" (sin importar mayúsculas/minúsculas).|
|13|Status Code (error)|400, 500|
|14|Response (error) 400|{"detail": "Error: Datos en [campos_vacios] no introducidos"}, {"detail": "Error: palabra string escrita en [campos_string]"}, o combinación: {"detail": "Error: Datos en [campos_vacios] no introducidos y palabra string escrita en [campos_string]"}|
|15|Response (error) 500|{"detail": "Error al insertar el contacto en la base de datos"}|
|16|Ejemplo Body|{"nombre": "Juan Pérez", "telefono": "5551234567", "email": "juan.perez@example.com"}|
|17|cURL|curl -X POST http://127.0.0.1:8000/v1/contactos -H "Content-Type: application/json" -d '{"nombre": "Juan Pérez", "telefono": "5551234567", "email": "juan.perez@example.com"}'|

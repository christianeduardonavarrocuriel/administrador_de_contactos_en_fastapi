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
|12|Status Code (error)|NA|
|13|Responsive Type (error)|NA|
|14|Response (error)|NA|
|15|cURL|curl -X GET http://127.0.0.1:8000/|
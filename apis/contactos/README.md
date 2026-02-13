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
|6|Query Param|limit:int&skip:int|
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


SQLite version 3.45.3 2024-04-15 13:34:05
Enter ".help" for usage hints.
sqlite> .mode csv
sqlite> .show
        echo: off
         eqp: off
     explain: auto
     headers: off
        mode: csv
   nullvalue: ""
      output: stdout
colseparator: ","
rowseparator: "\r\n"
       stats: off
       width: 
    filename: agenda.db
sqlite> .import data.csv contactos
sqlite> SELECT * FROM contactos;

- ""?"" Sirve para prevenir la inyección de código en SQL
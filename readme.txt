Scripts para generar feeds para subir a google reservas

Requisitos: 
* Instalar python para ejecutar los scripts en consola
* Actualizar los archivos dentro de entry/ cada vez que se hace una ejecución
  - lugares.json -> https://reservandonos.com/wp-json/webinfinitech/v1/get-data-places
  - metas.json -> https://reservandonos.com/wp-json/webinfinitech/v1/get-data-places-metas
  - sistema.json -> https://api.sistema.reservandonos.com/places/free?key=oZ6ETiG0eJIFwaeoskaqZJDh49SzFPkOw6xVCbtvZdruzA8lBDzTIWKQMIXhMs2XPUHXwyVbYHbUHzic5kJTFtGc2J5Lhlxvh8oeiM1rKI706ykwZeU4XiudtiywYirXfDcrO3Ki8QKLejJNRsNA3ALaOs34l8RHm3YpkTORW5nqGa2d5N9evaMKTRIjEF9au59UWgWVhJ95iJZz9rIDL86RjiOqHqufgDVliWOl0E4Hkb5QlDYIpYoHDZOkVtMB

Scripts:

Script para verificar errores (ejecutar desde directorio razi python validations/validations.py)
* validations.py
    Este script revisa la data de wordpress y del sistema de reservas para conseguir inconsistencia
    Genera los siguientes archivos dentro de la carpeta validations/:
     - list_lugares (listado de IDs del sistema de reserva con la carga completa en wordpress)
     - list_lugares_not (listado de IDs del sistema de reserva con data erronea o faltante en wordpress)
     - list_lugares_error (listado del nombre del lugar con una descripción de su error)
     - sistema_in (listado de IDs aceptados sin errores en wp ni en sistema)
     - sistema_not (listado de IDs de sistema de reserva con errores)
     - sistema_error (listado del nombre del lugar con una descripción su error)


Script para generar feeds
Merchants and Services

NOTA: dentro del json generado en la metadata para subir los datos pruebas debe ser:
    "processing_instruction": "PROCESS_AS_COMPLETE", con esto se borra los datos anteriores en google para subir nuevos lugares sin borrar los anteriores esto
    "processing_instruction": "PROCESS_AS_INCREMENTAL",

* single_merchant.py
 - Este script es manual cuando se desea agregar un solo lugar

* merchants.py (el que se debe usar para ir actualizando, revisar la NOTA de arriba)
  - Este script genera el feed de un listado de lugares, se debe agregar los IDs de wordpress de los lugares dentro del script en la variable 'list_lugares = []'
  - genera 2 archivos de salida dentro de output/ el merchantsXX.json y servicesXX.json (LOS QUE SE SUBEN A GOOGLE)

* all_merchants.py
  - Este script se uso para subir todos los lugares del sistema para verificar multiple errores
  - Dentro del codigo se puede poner un max de count para generar un número de lugares para pruebas
  - Genera el archivo listaccpet.txt con IDs aceptados para usar con all_availability.py
  - genera 2 archivos de salida dentro de output/ el merchantsXX.json y servicesXX.json (LOS QUE SE SUBEN A GOOGLE)

Availability

NOTA: en este script debe ser "PROCESS_AS_COMPLETE".
se debe crear politica de actualización de horarios por. ej cada domingo, o cada 15 días.. no puede ser mayor a un mes
cada generación se debe actualizar en el codigo -> fecha = '2019/11/26' y #definir fecha a 8 dias for i in range(0, 8):

* availability.py
  - genera todos los horarios uno por uno sin optimización de tamaño

* availability_recurrence (el que se debe usar para actualizar google reservas tener en cuenta los lugares )
  - genera archivo optimizado con parametro recurrente de horarios
  - se puede escoger manualmente los lugares a generar los horarios en la variable list_lugares = [] o se puede generar a partir del archivo listaccept.txt generado por all_merchants.py

* all_availability.py
  - archivo creado para recorrer todos los lugares y descubrir errores

  NOTA: los archivos se suben por sftp (se adjuntan)
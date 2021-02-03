# terminal-buses

Proyecto para prueba tecnica Destacame

Supuestos:

1.- La empresa que requiere este servicio solamente presta servicios para comunas del norte de chile
2.- Las compras de boletos solamente se hacen de forma presencial (por lo cual al final solamente aparecerá el total )
3.- Se considera la definicion de trayecto un viaje con origen y destino que se realiza a una hora en especifico
4.- Solo permite la creación de trayectos para el día siguiente del actual, al ser un servicio periodico, se debe ingresar una fecha de inicio y otra de final, junto a periodicidad , esto significa que el viaje se realizará todos los dias cada x tiempo donde x es la periodicidad ingresada.

Datos Importantes:

1.- Se deja habilitada una base de datos mysql para que puedan almacenar las consultas sin problema.
En caso de querer cambiar la bd una propia deben realizar los cambios ustedes.

2.- Se encuentra habilitado por CORS la direccion localhost:8080 (que es la ruta por defecto que entrega Vue), en caso de necesitar otra, favor añadir la direccion en terminal-buses -> back-buses -> admin -> settings.py y añadir o modificar el elemento CORS_ORIGIN_WHITELIST encontrado en la parte superior del archivo (para añadir nuevo elemento se debe añadir una , (coma), en caso de no tener)

3.- Se ocupa Python 3.8 para la elaboracion del back

4.- Instalar las dependencias del back con el comando pip install -r requirements.txt (debes estar posicionado en la carpeta admin que se encuentra en la ruta terminal-buses/back-buses/admin ) para ejecutar el comando

5 Instalar las dependencias del front con el comando npm i (debes estar posicionado en la carpeta front-buses que se encuentra en la raiz del proyecto ) para ejecutar el comando

6.- Levantar back Ejecutar comando python manage.py runserver en la carpeta terminal-buses/back-buses/admin

7.- Levantar Front Ejecutar comando (en otra terminal o pestaña de la consola ) npm run serve en en la carpeta terminal-buses/front-buses

USO
Para un flujo correcto se recomienda ingresar registros para Chofer (al oprimir las 3 lineas en la esquina superior derecha se debe desplegar un menú, allí hay una opción llamada mantenedor Chofer),

Luego de haber ingresado al Chofer se debe agregar un bus (repetir el proceso anterior y seleccionar mantenedor buses)

Al tener estos registros listos se puede proceder a crear un trayecto, dado que van a ser muchos viajes se tendrá que añadir el bus de forma manual a cada trayecto.

Compra Boletos / Viajes:

Esto se encuentra en la opcion Viajes dentro del menú.

Tener en cuenta si se crea un trayecto de Arica a Camarones, se debe crear uno de Camarones a Arica, en caso contrario aparecerá un mensaje avisando que no hay viajes disponibles

Tablas

Se crearon 5 Tablas para poder cumplir con la solucion

bus_bus
chofer_chofer
pasajero_pasajero
trayecto_trayecto
viaje_viaje

La plataforma no se encuentra terminada la 100% por temas laborales y personales, pero si tiene un porcentaje de avance alto, aunque falta un poco de validaciones, refactorizar codigo entre otros.

Espero las cosas que las cosas que las instrucciones que fueron mencionadas con anterioridad ayuden a ejecutar la aplicacion.

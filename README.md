# terminal-buses

Proyecto para prueba tecnica Destacame

Supuestos:

1.- La empresa que solicita el requerimiento solo presta servicios para comunas del norte de Chile.
2.- Las compras de boletos se realizan de forma presencial (por lo cual aparecerá solo el total final de la compra) y se almacenarán los datos del cliente.
3.- Se considera como definicion de trayecto, un viaje con origen y destino que se realiza a una hora en especifíco.
4.- Solo permite la creación de trayectos para el día siguiente del actual. Al ser un servicio periodico, se debe ingresar una fecha de inicio y una final, junto a su frecuencia. Esto significa que el viaje se realizará todos los dias cada x tiempo, donde x es la frecuencia ingresada.

Datos Importantes:

1.- Se habilita una base de datos MySQL para que se almacenen las consultas. En caso de querer cambiar la BD por una propia, deben realizar los respectivos cambios.

2.- Se encuentra habilitado por CORS la direccion localhost:8080 (que es la ruta por defecto que entrega Vue).
En caso de necesitar otra ruta seguir los pasos:

a). Añadir la direccion en terminal-buses -> back-buses -> admin -> admin ->settings.py.
b). Añadir o modificar el elemento CORS_ORIGIN_WHITELIST encontrado en la parte superior del archivo (Para añadir nuevo elemento, añadir una coma (,) en caso que no la tenga.)

3.- La elaboracion del back está construída con Python, versión 3.8.

4.- Instalar las dependencias del back con el comando "pip install -r requirements.txt". Para ejecutarlo, se necesita previamente estar posicionado en la carpeta "admin", que se encuentra en la ruta "terminal-buses/back-buses/admin". (se recomienda el uso de entornos virtuales)

5.- Instalar las dependencias del front con el comando "npm i". Para ejecutarlo, se necesita previamente estar posicionado en la carpeta "front-buses", que se encuentra en la raiz del proyecto.

6.- Levantar back: Ejecutar comando "python manage.py runserver" en la carpeta "terminal-buses/back-buses/admin".

7.- Levantar front: Ejecutar comando (en otra terminal o pestaña de la consola ) "npm run serve" en la carpeta "terminal-buses/front-buses".

USO
1.- Para un flujo correcto, presionar el botón de Menú (se encuentra en la esquina superior izquierda y tiene 3 líneas horizontales), seleccionar "Mantenedor Chofer" y luego "Nuevo chofer".

2.- Luego de haber ingresado al Chofer, agregar un bus (repetir el proceso anterior y seleccionar "Mantenedor Buses").

3.- Al tener estos datos ingresados, se puede crear un trayecto. Dado que serán muchos viajes, se tendrá que añadir el bus de forma manual para cada trayecto.

COMPRA BOLETOS / VIAJES

Esto se encuentra en la opcion Viajes dentro del menú.

Tener en cuenta que si se crea un trayecto de Arica a Camarones, se debe crear uno de Camarones a Arica. En caso contrario, aparecerá un aviso indicando que no hay viajes disponibles.

TABLAS

El sistema cuenta con 5 tablas para cumplir con los requerimientos solicitados:

bus_bus
chofer_chofer
pasajero_pasajero
trayecto_trayecto
viaje_viaje

Si bien la plataforma no se encuentra terminada al 100%, cuenta con un porcentaje de avance alto, quedando pendiente algunas pruebas de validaciones, optimización de codigo, entre otros.

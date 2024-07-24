Computacion 2 FINAL

#Carla S. Centeleghe
#Detector de Comidas

Descripción del Proyecto:

El proyecto consiste en una aplicación que permite a los clientes subir imágenes de comidas (carne o pizza) y el servidor responderá cual comida es.La aplicación utiliza una red neuronal de clasificación convuncional para distinguir entre carne y pizza.La arquitectura del proyecto es cliente-servidor e incluye el uso de sockets, mecanismos de IPC, tareas distribuidas con celery, intefaz en tking que utilia sockets, procesamiento de imagenes y guarda logs en redis (avisa de los mismos se guardaron por otro socket)

Funcionalidades:
- Cliente-Servidor con Sockets: Los clientes se conectan al servidor utilizando sockets para enviar imágenes y recibir resultados.
- Clasificación de Imágenes: El servidor utiliza una red neuronal para clasificar las imágenes y determinar cual es.
- Colas de Tareas Distribuidas: Se utiliza Celery para paralelizar la tarea de clasificación de imágenes.
- Compatibilidad con IPv4 e IPv6: El servidor maneja direcciones tanto IPv4 como IPv6.

- Interfaz de Usuario con Sockets: La aplicación incluye una interfaz en Tkinter la cual utiliza sockets par a la carga de imagenes. (Si no te conectas al servidor no te corre la intefaz)

- Guadado de logs: los logs de Flask y Celery se almacenan automatica mente en Redis, ademas se envia un mensaje al servidor. 



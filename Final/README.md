Computacion 2 FINAL

#Carla S. Centeleghe
#Detector de Gluten en Comidas

Descripción del Proyecto:

El proyecto consiste en una aplicación que permite a los clientes subir imágenes de comidas (carne o pizza) y el servidor responderá si la comida contiene gluten o no.La aplicación utiliza una red neuronal de clasificación binaria para distinguir entre carne y pizza, determinando si contienen gluten.La arquitectura del proyecto es cliente-servidor e incluye el uso de sockets, mecanismos de IPC, asincronismo de E/S, colas de tareas distribuidas, análisis de argumentos por línea de comandos y Celery para resolver tareas en paralelo.

Funcionalidades:
- Cliente-Servidor con Sockets: Los clientes se conectan al servidor utilizando sockets para enviar imágenes y recibir resultados.
- E/S Asíncrona: Cada conexión cliente-servidor se maneja de forma asíncrona usando hilos, permitiendo la concurrencia.
- Clasificación de Imágenes: El servidor utiliza una red neuronal para clasificar las imágenes y determinar si contienen gluten.
- Colas de Tareas Distribuidas: Se utiliza Celery para paralelizar la tarea de clasificación de imágenes.

- Compatibilidad con IPv4 e IPv6: El servidor maneja direcciones tanto IPv4 como IPv6.
- Mecanismos de IPC: Se implementan colas (Queues) para gestionar el acceso de los usuarios.
- Interfaz de Usuario: La aplicación incluye una interfaz 



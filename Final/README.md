# Computación 2 FINAL

## Carla S. Centeleghe
## Detector de Comidas

### Descripción del Proyecto

El proyecto consiste en una aplicación que permite a los clientes subir imágenes de comidas (carne o pizza) y el servidor responderá cuál comida es. La aplicación utiliza una red neuronal de clasificación convolucional para distinguir entre carne y pizza. La arquitectura del proyecto es cliente-servidor e incluye el uso de sockets, mecanismos de IPC, manejo de multiprogramacion, tareas distribuidas con Celery, procesamiento de imágenes y guarda logs en Redis.

### Funcionalidades

- **Cliente-Servidor**: Para que el cliente se conecte al servidor debe autentificarse.

- **Base de datos**: Los datos de ID y hora se guardan en la base de datos.

- **Cliente-Servidor**: Los clientes se conectan al servidor utilizando sockets para enviar imágenes y recibir resultados.

- **Clasificación de Imágenes**: El servidor utiliza una red neuronal para clasificar las imágenes y determinar si son carne o pizza.

- **Colas de Tareas Distribuidas**: Se utiliza Celery para paralelizar la tarea de clasificación de imágenes, permitiendo que las tareas se ejecuten en segundo plano y mejorando la eficiencia del sistema.

- **Compatibilidad con IPv4 e IPv6**: El servidor maneja direcciones tanto IPv4 como IPv6, asegurando compatibilidad con diferentes tipos de redes.

- **Guardado de Logs**: Los logs de todas las operaciones se almacenan automáticamente en Redis. Además, lo administra celery como tarea secundaria.



#Arquitectura General del Proyecto:

- Servidor: Flask para manejar peticiones HTTP.

- Sockets e interfaz: Para la comunicación en tiempo real entre clientes y servidor. Se utiliza en la interfaz grafica de tkinter

- Sockets y logs: Los logs de Flask y Celery se guardan en Redis y tambien le mandan un mensaje (cada log, un nuevo hilo) a server de socket 

- IPC: Usar colas de mensajes o pipes.

- Colas de tareas distribuidas: Usar Celery con un broker "Redis" 

- Red neuronal: red neuronal entrenado para identificar carne o pizza

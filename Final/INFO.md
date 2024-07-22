#Arquitectura General del Proyecto:

- Servidor: Flask para manejar peticiones HTTP.

- Sockets: Para la comunicación en tiempo real entre clientes y servidor. Ademas que se utiliza mucho en la interfaz grafica de tkinter

- IPC: Usar colas de mensajes o pipes.

- Colas de tareas distribuidas: Usar Celery con un broker "Redis" 

- Red neuronal: red neuronal entrenado para identificar carne o pizza

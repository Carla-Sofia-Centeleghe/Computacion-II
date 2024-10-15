#Arquitectura General del Proyecto:

- Servidor: Donde se procesan las peticiones del cliente

- Interfaz: Para la comunicación en tiempo real entre clientes y servidor, se utiliza en la interfaz grafica

- Logs: Los logs de se guardan y tambien le mandan un mensaje (cada log, un nuevo hilo) al server 

- IPv4 e IPV6: permite las coneciones del cliente

- Colas de tareas distribuidas: Usar Celery con un broker "Redis" 

- Red neuronal: red neuronal entrenado para identificar carne o pizza

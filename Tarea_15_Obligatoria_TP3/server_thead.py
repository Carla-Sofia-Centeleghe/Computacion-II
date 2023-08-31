#Carla S. Centeleghe 

#!/usr/bin/python3
import socket
import threading

def handle_client(connection): #Función para manejar la comunicación con un cliente
    print("Handling client...")
    
    while True:
        data = connection.recv(1024) #Recibe datos del cliente
        if data.decode() == '\r\n':
            continue
        else:
            message = data.decode()
            print("Received data: %s" % message)
            if message == "exit\r\n": #Verifica si se quiere cerrar la conexión
                response = "\nFarewell!\r\n".encode("utf-8")
                connection.send(response)
                print("The client terminated the connection.\r\n")
                connection.close()
                break
            else:
                response_msg = message.upper() + "\r\n" #Responde mensaje en mayúsculas
                connection.send(response_msg.encode("utf-8"))

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Crea un socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host_address = ""
    listening_port = 50001

    server_socket.bind((host_address, listening_port)) #Vincula el socket a la dirección y puerto especificados
    server_socket.listen(5) #Escucha conexiones entrantes, maximo de cola 5 pendientes

    print("Server listening on %s:%d" % (host_address, listening_port))
    
    while True:
        client_socket, client_address = server_socket.accept() #Acepta una conexión entrante y obtiene el socket del cliente con su dirección
        print("Connected to %s" % str(client_address))

        initial_msg = 'Appreciate your connection' + "\r\n" #Envia un mensaje de bienvenida al cliente
        client_socket.send(initial_msg.encode('ascii'))

        thread = threading.Thread(target=handle_client, args=(client_socket,))  #Inicia un nuevo subproceso para manejar al cliente
        thread.start()

if __name__ == "__main__":
    main()

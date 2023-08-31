#Carla S. Centeleghe 

#!/usr/bin/python3
import socket
import os
import sys
import signal

signal.signal(signal.SIGCHLD, signal.SIG_IGN) #Evito la creación de procesos zombis


#Función para manejar la comunicación con un cliente
def handle_client(client_socket, client_address):
    print("Connection from %s" % str(client_address))
    
    welcome_msg = "Thanks for connecting" + "\r\n" #Envia mensaje de bienbenida
    client_socket.send(welcome_msg.encode('ascii'))

    while True:
        try:
            msg = client_socket.recv(1024)  #Recibe un mensaje del cliente
            if not msg:
                break
            data = msg.decode()
            print("Received: %s" % data)
            if data == "exit\r\n": #Verifica si se quiere cerrar la conexión
                response = "\nGoodbye\r\n".encode("utf-8")
                client_socket.send(response)
                print("Client %s closed the connection\r\n" % str(client_address))
                break
            else:
                response_msg = data.upper() + "\r\n"   #Responde mensaje en mayúsculas
                client_socket.send(response_msg.encode("utf-8"))
        except BrokenPipeError:
            print("Client closed the connection")
            break
    
    client_socket.close()  #Cierra el socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Crea un socket del servidor
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Permite reutilizar la dirección
    
    host_address = ""  #Dirección del host 
    listening_port = 50002   #Puerto que escucha las conexiones
    
    server_socket.bind((host_address, listening_port))  #Vincula el socket a la dirección y puerto especificados
    server_socket.listen(5)   #Escucha conexiones entrantes, maximo de cola 5 pendientes
    print("Server listening on %s:%d" % (host_address, listening_port))
    
    while True:
        client_socket, client_address = server_socket.accept() #Acepta una conexión entrante y obtiene el socket del cliente con su dirección
        child_pid = os.fork()  #Proceso hijo que maneja la comunicación con este cliente
        if child_pid == 0:
            server_socket.close()  #Proceso hijo: ceiera el socket del servidor y manejar al cliente
            handle_client(client_socket, client_address)
            sys.exit(0)
        else:
            client_socket.close()  #Proceso padre: ciera el socket del cliente 

if __name__ == "__main__":
    main()
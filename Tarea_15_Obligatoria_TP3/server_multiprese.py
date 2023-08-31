#Carla S. Centeleghe 

#!/usr/bin/python3
import socket
import multiprocessing

def handle_client(client_socket, client_address):
    print("Connection from %s" % str(client_address))
    
    welcome_msg = "Thanks for connecting" + "\r\n" #Envia un mensaje de bienvenida
    client_socket.send(welcome_msg.encode('ascii'))
    
    while True:
        try:
            msg = client_socket.recv(1024) #Recibe un mensaje del cliente
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
                response_msg = data.upper() + "\r\n" #Responde mensaje en mayúsculas
                client_socket.send(response_msg.encode("utf-8"))
        except BrokenPipeError:
            print("Client closed the connection")
            break
    
    client_socket.close() #Cierra el socket

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Crea un socket del servidor
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Permite reutilizar la dirección

    host_address = ""  #Dirección del host 
    listening_port = 50001 #Puerto que escucha las conexiones

    server_socket.bind((host_address, listening_port)) #Vincula el socket a la dirección y puerto especificados
    server_socket.listen(5) #Escucha conexiones entrantes, maximo de cola 5 pendientes
    print("Server listening on %s:%d" % (host_address, listening_port))
    
    pool = multiprocessing.Pool(processes=4) #Crea un grupo de procesos para manejar múltiples clientes

    while True:
        client = server_socket.accept() #Acepta una conexión entrante y obtiene el socket del cliente con su dirección
        client_socket, client_address = client  

        print("Connected to %s" % str(client_address))
        initial_msg = 'Thanks for connecting' + "\r\n"    #Envia un mensaje de bienvenida al cliente
        client_socket.send(initial_msg.encode('ascii'))

        pool.apply_async(handle_client, (client_socket, client_address))  #Inicia un nuevo proceso para manejar el cliente

if __name__ == "__main__":
    main()

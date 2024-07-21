import socket
import multiprocessing

print(dir(socket))

def handle_client(client_socket):   # Función para manejar la conexión del cliente
    request = client_socket.recv(1024).decode()
    print(f"Recibido: {request}")
    client_socket.send("ACK!".encode())   # Enviar una respuesta al cliente
    client_socket.close()    # Cerrar la conexión

def server_loop():  # Función para iniciar el servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crear un socket 
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Esperando conexiones...")
    while True:        # Bucle para aceptar conexiones
        client_sock, addr = server.accept()
        print(f"Conexión aceptada de: {addr}")  
        client_handler = multiprocessing.Process(target=handle_client, args=(client_sock,))     # Crear un proceso para manejar la conexión del cliente
        client_handler.start()  # Iniciar el proceso

if __name__ == "__main__":
    server_loop()

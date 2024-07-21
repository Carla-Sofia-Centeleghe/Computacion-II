import socket
import multiprocessing

import socket
print(dir(socket))

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    print(f"Recibido: {request}")
    client_socket.send("ACK!".encode())
    client_socket.close()

def server_loop():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Esperando conexiones...")
    while True:
        client_sock, addr = server.accept()
        print(f"Conexión aceptada de: {addr}")
        client_handler = multiprocessing.Process(target=handle_client, args=(client_sock,))
        client_handler.start()

if __name__ == "__main__":
    server_loop()

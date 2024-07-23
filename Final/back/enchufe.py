import socket
import threading

def handle_client(client_socket):
    try:
        # Recibir datos del cliente (imagen en este caso)
        image_data = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet:
                break
            image_data += packet

        client_socket.sendall(b"Imagen recibida y procesada")
    except Exception as e:
        client_socket.sendall(f"Error: {e}".encode('utf-8'))
    finally:
        client_socket.close()

def server_loop():      #Solo IP4 por ahora
    # Crear socket para IP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))      #Cambiar por (("::", 9999))
    server.listen(5)
    print("Esperando conexiones...")
    while True:
        client_sock, addr = server.accept()
        print(f"Conexión aceptada de: {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_sock,))
        client_handler.start()

if __name__ == "__main__":
    server_loop()

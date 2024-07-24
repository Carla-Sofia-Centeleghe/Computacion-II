import socket
import threading # Para manejar múltiples conexiones, multiples hilos 
import sys 

def handle_client(client_sock):
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            print(f"Mensaje: {data.decode()}")
    finally:
        client_sock.close()

def server_loop():     
    HOST = None  # Significa todas las interfaces disponibles
    PORT = 9999  # Puerto para escuchar 
    
    # Intenta crear un socket para cada dirección disponible y usar el primero que funcione
    # Uso de socket.getaddrinfo para soportar IPv4 e IPv6, ademas de sockt no especificado
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            print(f"Error al crear el socket: {msg}")
            continue
        try:
            s.bind(sa)
            s.listen(5)
            print(f"Servidor escuchando en {sa}")
            break  # El socket fue creado exitosamente
        except OSError as msg:
            print(f"Error al abrir el socket: {msg}")
            s.close()
            continue
    
    if s is None:
        print('No se pudo abrir el socket')
        sys.exit(1)
    
    print("Esperando conexiones...")
    
    while True:
        client_sock, addr = s.accept()
        print(f"Aceptada conexión desde: {addr}")
        threading.Thread(target=handle_client, args=(client_sock,)).start()

if __name__ == "__main__":
    server_loop()
    #handle_client()

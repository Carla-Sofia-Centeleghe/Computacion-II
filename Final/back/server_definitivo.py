import os
import socket
import threading
import uuid
import argparse
from querys import consulta
from celery_app import classify_image_task
from celery_app import log 
from multiprocessing import Queue

result_queue = Queue()
logger = log 

# Configuración inicial
SERVER = socket.gethostbyname(socket.gethostname())
DISCONNECT_MESSAGE = b"disconnect"

def handle_client(conn, addr):
    connected = True
    id_con = uuid.uuid1().int
    id_con /= 1000000
    consulta(id_con)
    
    while connected:
        try:
            msg_type = conn.recv(100).decode(FORMAT)
            if msg_type == DISCONNECT_MESSAGE.decode(FORMAT):
                conn.send(b"Disconnect".encode(FORMAT))
                conn.close()
                connected = False
                break
            
            print(f"Usuario {addr} dice {msg_type}")
            
            # Manejar diferentes tipos de mensajes
            if msg_type == "I":
                # Mensaje de imagen
                filepath_length = int(conn.recv(HEADER).decode(FORMAT))
                filepath = conn.recv(filepath_length).decode(FORMAT)
                
                if not os.path.exists(filepath):
                    conn.send("Archivo no encontrado".encode(FORMAT))
                    logger(f"Archivo no encontrado: {filepath}")
                    continue
                
                print("Ruta de archivo recibida, procesando...")
                logger(f"Archivo seleccionado: {filepath}")
                
                result = classify_image_task.apply_async(args=[filepath])
                result_queue.put(result)

                classification = result.get(timeout=10)
                conn.send(classification.encode(FORMAT))
                print(f"Clasificación enviada al cliente: {classification}")
                logger(f"Clasificación recibida: {classification}")
            elif msg_type == "T":
                # Mensaje de texto
                message = conn.recv(int(conn.recv(HEADER).decode(FORMAT))).decode(FORMAT)
                print(f"Texto recibido: {message}")
                conn.send(message.encode(FORMAT))
        except Exception as e:
            print(f"Error en el cliente: {e}")
            conn.close()
            break

def start_server():
    host = None  # Symbolic name meaning all available interfaces

    for res in socket.getaddrinfo(host, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = None
            for l in ['IPv6', 'IPv4']:
                if af == socket.AF_INET6:
                    addr = ('::', 0)  # IPv6
                elif af == socket.AF_INET:
                    addr = ('', PORT)  # IPv4
                else:
                    continue

                try:
                    s = socket.socket(af, socktype, proto)
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    s.bind(addr)
                    s.listen(1)
                    print(f'Servidor escuchando en {addr}')
                    logger(f'Servidor escuchando en {addr}')

                    while True:
                        conn, addr = s.accept()
                        print(f'Conexión establecida desde {addr}')
                        logger(f'Conexión establecida desde {addr}')

                        threading.Thread(target=handle_client, args=(conn, addr)).start()

                except socket.error as e:
                    print(f"Error al crear socket {e}")
                    logger(f"Error al crear socket {e}")
                    break

        except socket.gaierror:
            continue

    if not s:
        print('No se pudo encontrar una dirección adecuada')
        logger('No se pudo encontrar una dirección adecuada')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Servidor de red con soporte para IPv4 e IPv6')
    parser.add_argument('--x', type=int, default=8080, help='Numero de puerto (default: 8080)')
    parser.add_argument('--y', type=str, default="Desconectado", help='Mensaje de desconexión (default: "Desconectado")')
    parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
    args = parser.parse_args()

    #PORT = str(args.port)
    HEADER = 64
    PORT = args.x
    FORMAT = args.z

    try:
        start_server()
    except KeyboardInterrupt:
        print("Servidor cerrando...")
        logger("Servidor cerrando...")



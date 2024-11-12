import os
import socket
import threading
import uuid
import argparse
from querys import consulta
from celery_app import classify_image_task
from celery_app import log 
from multiprocessing import Queue
from querys import consulta

result_queue = Queue()
logger = log 


DISCONNECT_MESSAGE = b"DISCONNECT"  # Utilizamos bytes para DISCONNECT_MESSAGE
parser=argparse.ArgumentParser()
parser.add_argument('--x',type=int,default=8080,help='Numero de puerto')
parser.add_argument('--y',type=str,default='quit',help='Mensaje de desconexion')
parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')
args=parser.parse_args()

HEADER = 64
PORT = args.x
FORMAT = args.z
SERVER = socket.gethostbyname(socket.gethostname())

def handle_client(conn, addr, access):
    connected = True
    id_con = uuid.uuid1().int
    id_con /= 1000000
    consulta(id_con)
    
    while connected:
        try:
            msg_type = conn.recv(1).decode(FORMAT)
            if msg_type == DISCONNECT_MESSAGE.decode(FORMAT):
                conn.send(b"Disconnect".encode(FORMAT))
                conn.close()
                semaphore.release()         # Libera el semaforo para permitir otra conexion
                connected = False
                break
            
            if access == False:
                conn.send(f"Disconnect capacity".encode(FORMAT))
                conn.close()
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

semaphore=threading.BoundedSemaphore(2)  # Define semaforo para controlar la cantidad de conexiones, maximo 2 

ADDR2 = ("", PORT)
server_ipv6 = socket.create_server(ADDR2, family=socket.AF_INET6, dualstack_ipv6=True)
SERVER=socket.gethostbyname(socket.gethostname())
 
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER,PORT)
    
server_ipv4=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#server_ipv4.bind(ADDR)        
        
def start_server():
    print("Servidor escuchando...")
    logger("Servidor escuchando...")
    server_ipv6.setblocking(0)
    server_ipv6.listen()
    server_ipv4.setblocking(0)
    server_ipv4.listen()

    while True:

        try:
            conn_ipv4, addr_ipv4 = server_ipv4.accept()
            print(f"Nuevo cliente IPv4 conectado. Direccion {addr_ipv4}")
            access = semaphore.acquire(blocking=False)
            threading.Thread(target=handle_client, args=(conn_ipv4, addr_ipv4, access)).start()
        except:
            pass
        try:
            conn_ipv6, addr_ipv6 = server_ipv6.accept()
            print(f"Nuevo cliente IPv6 conectado. Direccion {addr_ipv6}")
            logger(f"Nuevo cliente IPv6 conectado. Direccion {addr_ipv6}")
            access = semaphore.acquire(blocking=False)
            threading.Thread(target=handle_client, args=(conn_ipv6, addr_ipv6, access)).start()
        except:
            pass


start_server()
    
def main(args):
    global PORT, DISCONNECT_MESSAGE, FORMAT
    PORT = args.x
    DISCONNECT_MESSAGE = args.y
    FORMAT = args.z
    start_server()

main(args)


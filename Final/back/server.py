from email import message
import os
import socket # Importamos la librería socket para manejar la conexión
import threading # Importamos la librería threading para manejar múltiples conexiones
import uuid # Importamos la librería uuid para generar un identificador único
import celery
#import cv2 # Importamos la librería cv2 para procesar imágenes
import argparse
from celery_app import classify_image_task, log 
import keras #tpye: ignore
from PIL import Image
import numpy as np

from querys import consulta
from celery_app import log 

#from cliente_IPV4 import start_server
#from cliente_IPV6 import start_server
from celery import Celery

# Función para manejar la conexión con el cliente
def main(args):
    HEADER = 64                     # Tamaño del encabezado
    PORT = args.x                   # Puerto de conexión
    DISCONNECT_MESSAGE = args.y     # Mensaje de desconexión
    FORMAT = args.z                 # Formato de codificación

    # Configuramos el servidor y el semaforo
    semaphore = threading.BoundedSemaphore(2)

    ADDR2 = ("", PORT)
    server_ipv6 = socket.create_server(ADDR2, family=socket.AF_INET6, dualstack_ipv6=True)
    server_ipv6.bind(ADDR)

    SERVER=socket.gethostbyname(socket.gethostname())
    ADDR=(SERVER,5051)
    
    server_ipv4=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_ipv4.bind(ADDR)


# Funcion para manejar el cliente conectado
def handle_client(conn, addr, HEADER, FORMAT, DISCONNECT_MESSAGE):
    connected = True
    id_con = uuid.uuid1().int // 1000000
    consulta(id_con)  # Registramos la conexión en la base de datos
    data = conn.recv(1024)
    if not data:
        log("No se recibió ningún dato del cliente.")
        return

    try:    
        while connected:
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    
                    if msg == DISCONNECT_MESSAGE:
                        conn.send("Desconectado".encode(FORMAT))
                        connected = False
                        conn.close()
                        break
                file_path = data.decode()
                log(f"Archivo recibido: {file_path}")
                if os.path.exists(file_path):
            # Enviar tarea a Celery
                    result = classify_image_task.delay(file_path)
                    conn.send(f"Tarea enviada a Celery con ID: {result.id}".encode())
                    log(f"Tarea enviada a Celery con ID: {result.id}")
                else:
                    conn.send("File not found".encode())
                    log(f"Archivo no encontrado: {file_path}")
   
    except Exception as e:
            print(f"Error en la conexión con el cliente {addr}: {str(e)}")
    

# Función de clasificación de imagen que será ejecutada por Celery
# Configuración de Celery
celery_app = Celery('tasks', broker='redis://localhost:6379')

@celery_app.task(name="app.classify_image")
def classify_image_task(filepath):
    try:
        model = keras.models.load_model('simple_cnn_model.keras')
        img = Image.open(filepath)
        img = img.resize((150, 150))
        img_array = np.expand_dims(np.array(img), axis=0)
        predictions = model.predict(img_array)
        result = 'Pizza' if predictions[0] > 0.5 else 'Carne'
        log(f"Resultado de clasificación: {result}")
        return result
    except Exception as e:
        log(f"Error al procesar la imagen: {e}")
        return f"Error processing image: {e}"
    

# Funcion prar establecer la conexion con servidor
def start_server(server_ipv4, server_ipv6, semaphore):
        print("Servidor escuchando...")
        server_ipv4.setblocking(0)
        server_ipv6.setblocking(0)
        server_ipv6.listen()

        while True:
            try:
                conn_ipv4, addr_ipv4 = server_ipv4.accept()
                print(f"Nuevo cliente IPv4 conectado. Dirección {addr_ipv4}")
                access = semaphore.acquire(blocking=False)
                threading.Thread(target=handle_client, args=(conn_ipv4, addr_ipv4, access)).start()
            except socket.error as e:
                print(f"Error al aceptar conexión IPv4: {str(e)}")

            try:
                conn_ipv6, addr_ipv6 = server_ipv6.accept()
                print(f"Nuevo cliente IPv6 conectado. Dirección {addr_ipv6}")
                access = semaphore.acquire(blocking=False)
                threading.Thread(target=handle_client, args=(conn_ipv6, addr_ipv6, access)).start()

            except socket.error as e:
                print(f"Error al aceptar conexión IPv6: {str(e)}")

            start_server(server_ipv4, server_ipv6, semaphore)    

# Configuración de argumentos para el servidor
parser = argparse.ArgumentParser()
parser.add_argument('--x', type=int, default=8080, help='Número de puerto')
parser.add_argument('--y', type=str, default='quit', help='Mensaje de desconexión')
parser.add_argument('--z', type=str, default='utf-8', help='Formato de codificación')
args = parser.parse_args()

main(args)
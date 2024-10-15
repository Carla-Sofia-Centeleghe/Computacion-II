import socket
import threading # Para manejar múltiples conexiones, multiples hilos 
import sys # Para manejar errores
import os
from tensorflow import keras # type: ignore
import tensorflow as tf # type: ignore
from PIL import Image
import numpy as np
from celery_config import celery
from celery_config import log 
from werkzeug.utils import secure_filename

def handle_client(client_sock):
    try:
        while True:
            data = client_sock.recv(1024)
            if not data:
                log("No se recibió ningún dato del cliente.")
                return

            # Aquí debes recibir la imagen, procesarla y devolver el resultado
            file_path = data.decode()
            log(f"Archivo recibido: {file_path}")
            if os.path.exists(file_path):
            # Enviar tarea a Celery
                result = classify_image_task.delay(file_path)
                client_sock.send(f"Tarea enviada a Celery con ID: {result.id}".encode())
                log(f"Tarea enviada a Celery con ID: {result.id}")
            else:
                client_sock.send("File not found".encode())
                log(f"Archivo no encontrado: {file_path}")
    except Exception as e:
        log(f"Error al procesar cliente: {e}")
    finally:
        client_sock.close()

# Función de clasificación de imagen que será ejecutada por Celery
@celery.task(name="app.classify_image")
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
    
def server_loop():     
    HOST = '0.0.0.0' # Significa todas las interfaces disponibles
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

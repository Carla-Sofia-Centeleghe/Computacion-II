import threading
import tkinter as tk
from tkinter import Tk, filedialog, Label, Button, ttk, messagebox, Canvas, PhotoImage
from PIL import Image, ImageTk
import socket
import os
from celery_app import classify_image_task, log
from querys import consulta
import argparse
import uuid
import numpy as np
from tensorflow import keras #tpye: ignore
from celery import Celery

# Configuración de argumentos para el servidor
parser = argparse.ArgumentParser()
parser.add_argument('--x', type=int, default=8080, help='Número de puerto')
parser.add_argument('--y', type=str, default='quit', help='Mensaje de desconexión')
parser.add_argument('--z', type=str, default='utf-8', help='Formato de codificación')
args = parser.parse_args()

# Configuración del cliente
CLIENT_IP = '127.0.0.1'
CLIENT_PORT = 9999

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

class SemaphoreManager:
    def __init__(self):
        self.semaphore = threading.BoundedSemaphore(2)

    def acquire(self):
        return self.semaphore.acquire(blocking=False)

    def release(self):
        self.semaphore.release()

semaphore_manager = SemaphoreManager()

def handle_client(conn, addr, HEADER, FORMAT, DISCONNECT_MESSAGE, semaphore):
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
                    result = classify_image_task.delay(file_path)
                    conn.send(f"Tarea enviada a Celery con ID: {result.id}".encode())
                    log(f"Tarea enviada a Celery con ID: {result.id}")
                else:
                    conn.send("File not found".encode())
                    log(f"Archivo no encontrado: {file_path}")
    except Exception as e:
        print(f"Error en la conexión con el cliente {addr}: {str(e)}")

def send_image_to_server(image_path):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((CLIENT_IP, CLIENT_PORT))
            s.send(image_path.encode())

            # Recibe la respuesta con el ID de tarea
            task_id = s.recv(1024).decode()

            # Mostrar imagen de clasificación
            classified_img_path = "pizza_image.png" if task_id == "Pizza" else "carne_image.png"
            img = Image.open(classified_img_path)
            img = img.resize((150, 150))  # Cambiar el tamaño de la imagen para la visualización
            img_tk = ImageTk.PhotoImage(img)
            root.after(0, lambda: image_label.config(image=img_tk), image_label)
            root.after(0, lambda img=img_tk: image_label.config(image=img))

    except Exception as e:
        messagebox.showerror("Error", f"Error en la conexión: {e}")

def upload_and_classify():
    if not file_path:
        messagebox.showerror("Error", "No se ha seleccionado ningún archivo")
        return
    
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "El archivo no se ha encontrado")
        return
    
    threading.Thread(target=send_image_to_server, args=(file_path,), daemon=True).start()

root = tk.Tk()
root.title("Detector de Comida")
root.geometry("400x500")

label = Label(root, text="Por favor, seleccione un archivo", font=("Arial", 12))
label.pack(pady=10)

image_label = Label(root)  # Mostrar la imagen
image_label.pack(pady=10)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10)

select_button = Button(root, text="Seleccionar Archivo", command=lambda: select_file())
select_button.pack(pady=5)

upload_button = Button(root, text="Subir y Clasificar", command=upload_and_classify)
upload_button.pack(pady=5)

file_path = None

def select_file():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:
        label.config(text=f"Archivo seleccionado: {os.path.basename(file_path)}")
        log(f"Archivo seleccionado: {file_path}")
        preview_image()  # Previsualizar la imagen
    else:
        label.config(text="No se ha seleccionado ningún archivo")
        log("No se seleccionó ningún archivo.")

def preview_image():
    try:
        img = Image.open(file_path)
        img = img.resize((150, 150))  # Cambiar el tamaño de la imagen para la previsualización
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Mantener una referencia de la imagen
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar la imagen: {e}")
        log(f"Error al cargar la imagen: {e}")

if __name__ == "__main__":
    semaphore_manager = SemaphoreManager()
    HEADER = 64
    PORT = args.x
    DISCONNECT_MESSAGE = args.y
    FORMAT = args.z

    ADDR = ("", PORT)
    server_ipv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ipv4.bind(ADDR)
    server_ipv4.listen()

    print("Servidor escuchando...")
    server_ipv4.setblocking(0)

    while True:
        try:
            conn, addr = server_ipv4.accept()
            print(f"Nuevo cliente conectado. Dirección {addr}")
            access = semaphore_manager.acquire(blocking=False)
            threading.Thread(target=handle_client, args=(conn, addr, HEADER, FORMAT, DISCONNECT_MESSAGE, semaphore_manager)).start()
        except socket.error as e:
            print(f"Error al aceptar conexión: {str(e)}")

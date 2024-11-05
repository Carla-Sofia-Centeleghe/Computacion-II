import threading
import tkinter as tk
from tkinter import Tk, filedialog, Label, Button, ttk, messagebox, Canvas, PhotoImage
from PIL import Image, ImageTk
import socket
import os
from celery_app import classify_image_task
#import logging

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__) 
from celery_app import log 
logger = log 

class FoodDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Comida")
        self.root.geometry("400x500")

        self.label = Label(root, text="Por favor, seleccione un archivo", font=("Arial", 12))
        self.label.pack(pady=10)

        self.image_label = Label(root)  # Mostrar la imagen
        self.image_label.pack(pady=10)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.select_button = Button(root, text="Seleccionar Archivo", command=self.select_file)
        self.select_button.pack(pady=5)

        self.upload_button = Button(root, text="Subir y Clasificar", command=self.upload_and_classify)
        self.upload_button.pack(pady=5)

        self.file_path = None
        self.classified_image_label = Label(root)  # Mostrar la imagen clasificada
        self.classified_image_label.pack(pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.label.config(text=f"Archivo seleccionado: {os.path.basename(self.file_path)}")
            logger(f"Archivo seleccionado: {self.file_path}")
            self.preview_image()  # Previsualizar la imagen
        else:
            self.label.config(text="No se ha seleccionado ningún archivo")
            logger("No se seleccionó ningún archivo.")

    def preview_image(self):
        try:
            img = Image.open(self.file_path)
            img = img.resize((150, 150))  # Cambiar el tamaño de la imagen para la previsualización
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk  # Mantener una referencia de la imagen
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {e}")
            logger(f"Error al cargar la imagen: {e}")

    def upload_and_classify(self):
        if not self.file_path:
            messagebox.showerror("Error", "No se ha seleccionado ningún archivo")
            logger("Intento de clasificación sin seleccionar archivo.")
            return
        
        if not os.path.exists(self.file_path):
            messagebox.showerror("Error", "El archivo no se ha encontrado")
            logger(f"Archivo no encontrado: {self.file_path}")
            return
        
        # Inicia la barra de progreso
        self.progress["value"] = 0
        self.root.update_idletasks()

        # Hilo para manejar la conexión con el servidor
        threading.Thread(target=self.send_image_to_server, daemon=True).start()

    def send_image_to_server(self):
        try:
            self.progress["value"] = 20
            self.root.update_idletasks()

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', 9999))  # Cambiar IP según sea necesario
                s.send(self.file_path.encode())

                self.progress["value"] = 50
                self.root.update_idletasks()

                # Recibe la respuesta con el ID de tarea
                task_id = s.recv(1024).decode()
                self.progress["value"] = 100
                self.root.update_idletasks()

                messagebox.showinfo("Tarea enviada", f"ID de la tarea: {task_id}", "Resultado", f"Clasificación: {classify_image_task.result}")
                logger(f"Clasificación recibida: {classify_image_task.result}")
                logger(f"ID de tarea recibido: {task_id}")

                 # Mostrar imagen de clasificación
                self.display_classified_image(classify_image_task.result)

        except Exception as e:
            messagebox.showerror("Error", f"Error en la conexión: {e}")
            logger(f"Error en la conexión con el servidor: {e}")
        finally:
            self.progress["value"] = 0
            self.root.update_idletasks()

    def display_classified_image(self, classification):
        # Cargar y mostrar la imagen según la clasificación
        classified_img_path = "pizza_image.png" if classification == "Pizza" else "carne_image.png"
        try:
            img = Image.open(classified_img_path)
            img = img.resize((150, 150))  # Cambiar el tamaño de la imagen para la visualización
            img_tk = ImageTk.PhotoImage(img)
            self.classified_image_label.config(image=img_tk)
            self.classified_image_label.image = img_tk  # Mantener una referencia de la imagen
            self.classified_image_label.pack()
        except Exception as e:
            logger(f"Error al cargar la imagen de clasificación: {e}")

if __name__ == "__main__":
    root = Tk()
    app = FoodDetectorApp(root)
    root.mainloop()
 

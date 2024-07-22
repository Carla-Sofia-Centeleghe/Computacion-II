import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import socket
from PIL import Image, ImageTk

class App:
     # Configuración de la interfaz de Tkinter
    def __init__(self, root):

        self.root = root
        self.root.title("Food Detector")
        # Configuración del socket
        self.server_ip = '127.0.0.1'
        self.server_port = 9999
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack(padx=10, pady=10)

        self.file_label = tk.Label(frame, text="No se ha seleccionado un archivo", width=50)
        self.file_label.pack(pady=(0, 10))

        select_button = tk.Button(frame, text="Seleccionar archivo", command=self.select_file)
        select_button.pack(side=tk.LEFT, padx=(0, 10))

        upload_button = tk.Button(frame, text="Subir y Clasificar", command=self.upload_file)
        upload_button.pack(side=tk.RIGHT)

    def connect_to_server(self):
            try:
                self.socket.connect((self.server_ip, self.server_port))
                print("Conectado al servidor")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.file_label.config(text=file_path)
            self.show_image(file_path)
        else:
            self.file_label.config(text="No se ha seleccionado un archivo")

    def show_image(self, file_path):
        image = Image.open(file_path)
        #image = image.resize((300, 450), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.file_label.config(image=photo)
        self.file_label.image = photo

    def upload_file(self):
        file_path = self.file_label.cget("text")
        if file_path == "No se ha seleccionado un archivo":
            messagebox.showerror("Error", "Por favor selecciona primero un archivo")
            return
        
        url = 'http://localhost:5000/upload'  # URL del servidor Flask
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(url, files=files)
                response.raise_for_status()
                task_id = response.json().get("task_id")
                if task_id:
                    self.check_result(task_id)
                else:
                    messagebox.showerror("Error", "No se pudo obtener el ID de la tarea")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

    def check_result(self,task_id):
        url = f'http://localhost:5000/result/{task_id}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            result = response.json()
            if result['state'] == 'PENDING':
                self.root.after(2000, lambda: self.check_result(task_id))  # Verifica el estado cada 2 segundos
            else:
                messagebox.showinfo("Resultado", f"Resultado de la Clasificación: {result.get('result', 'Desconocido')}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"No se pudo obtener el resultado: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

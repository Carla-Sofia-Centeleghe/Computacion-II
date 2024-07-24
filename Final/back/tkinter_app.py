import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk 
import requests
import socket
import threading
import redis
import logging
from PIL import Image, ImageTk

class App:
    def __init__(self):
        #self.root = tk.Tk()
        self.successful_connection = self.connect_to_server()
        if self.successful_connection:
            self.root = tk.Tk()
            self.event_interface = Event(self.root)
            self.root.mainloop()
    def connect_to_server(self):
        self.server_ip = 'localhost'
        self.server_port = 9999
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for res in socket.getaddrinfo(self.server_ip, self.server_port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.socket = socket.socket(af, socktype, proto)
                self.socket.connect(sa)
                print("Conectado al servidor")
                return True  # Conexión exitosa
            except OSError as e:
                print(f"No se pudo conectar al servidor: {e}")
                self.socket.close()
        messagebox.showerror("Error", "No se pudo conectar al servidor.")
        return False  # Conexión fallida
    

    
    # Configuración de la interfaz de Tkinter 
class Event:
        def __init__(self, root):
            self.root = root
            self.root.title("Food Detector")
            frame = tk.Frame(root, padx=10, pady=10)
            frame.pack(padx=10, pady=10)

            self.file_label = tk.Label(frame, text="No se ha seleccionado un archivo", width=50)
            self.file_label.pack(pady=(0, 10))

            select_button = tk.Button(frame, text="Seleccionar archivo", command=self.select_file)
            select_button.pack(side=tk.LEFT, padx=(0, 10))

            upload_button = tk.Button(frame, text="Subir y Clasificar", command=self.upload_file)
            upload_button.pack(side=tk.RIGHT)
            
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

            # Crear barra de progreso, porqué la clasificación puede tardar timpo
            # La barra de progeso aparece DOS p**tas veces, PREGUNTAR AL PROFE
            self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=200, mode="indeterminate")
            self.progress_bar.pack(pady=(0, 20)) 
            self.progress_bar.start()

            try:
                response = requests.get(url)
                response.raise_for_status()
                result = response.json()
                if result['state'] == 'PENDING':
                    self.root.after(2000, lambda: self.check_result(task_id))  # Verifica el estado cada 2 segundos
                else:
                    # Finaliza la barra de progreso, igual la muy HPD no se cierra, PREGUNTAR AL PROFE
                    try:
                        self.progress_bar.stop()
                        self.progress_bar.destroy()
                    finally:        # Muestar el resultado
                        messagebox.showinfo("Resultado", f"Resultado de la Clasificación: {result.get('result', 'Desconocido')}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"No se pudo obtener el resultado: {e}")

class RedisHandler(logging.Handler):
    def __init__(self, host='localhost', port=6379, db=0, channel='logs', server_host='localhost', server_port=9999):
        super().__init__() #(self)
        self.client = redis.StrictRedis(host=host, port=port, db=db)
        self.channel = channel
        
        # Configuración del socket para enviar mensajes al servidor
        self.server_host = server_host
        self.server_port = server_port
        self.server_socket = self.connect_to_server()

    def connect_to_server(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.server_host, self.server_port))
            #s.sendall(log_entry.encode())
            return s
        except Exception as e:
            print(f"Error al conectar con el servidor: {e}")
            return None

    def emit(self, record):
        log_entry = self.format(record)
        self.client.rpush(self.channel, log_entry)
        # Crear hilo para enviar el log al servidor
        threading.Thread(target=self.send_log_to_server, args=(log_entry,)).start()

    def send_log_to_server(self, log_entry):
        server_socket = self.connect_to_server()
        if server_socket:
            try:
                server_socket.sendall(f'Log guardado: {log_entry}'.encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje al servidor: {e}")
            finally:
                server_socket.close()

if __name__ == "__main__":
    app = App()
    #rendis_handler = RedisHandler()
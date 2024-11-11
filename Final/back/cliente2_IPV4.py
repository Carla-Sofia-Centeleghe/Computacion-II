import socket
import argparse
from multiprocessing import Queue
from autentificacion import main_log_process
from PIL import Image
import io
import os

try:
    # Intenta importar tkinter para usar el cuadro de diálogo
    import tkinter as tk
    from tkinter import filedialog
    tkinter_available = True
except ImportError:
    tkinter_available = False

def main(args):
    usuarios_queue = Queue()
    contraseñas_queue = Queue()

    def login():
        usuario = input("Usuario: ")
        contraseña = input("Clave: ")

        usuarios_queue.put(usuario)
        contraseñas_queue.put(contraseña)
    
        log = main_log_process(usuarios_queue.get(), contraseñas_queue.get())
        return log
    
    access = login()  

    if access:
        print("Logeo exitoso!")
        HEADER = 64
        PORT = args.x
        FORMAT = args.z
        SERVER = socket.gethostbyname(socket.gethostname()) # Obtenemos la dirección IP del servidor
        ADDR = (SERVER, PORT)                                # Creamos una tupla con la dirección IP y el puerto  
        CONNECTED = True
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creamos un socket para la conexión
        try:
            client.connect(ADDR)                                   # Conectamos el cliente al servidor
            print(f"Intentando conectar a {ADDR}")
            client.settimeout(5)  # Establecer un tiempo de espera para la conexión
            connected = True
            while connected:
                if tkinter_available:
                    root = tk.Tk()
                    root.withdraw()  # Ocultar ventana principal
                    msg = filedialog.askopenfilename(title="Seleccionar imagen", filetypes=[("Imagenes", "*.jpg *.jpeg *.png")])
                    root.destroy()
                else:
                    msg = input("Ingrese el nombre o la ruta completa de la foto: ")

                if not msg or not os.path.isfile(msg):
                    print("La imagen no se encontró. Intente nuevamente.")
                    continue
        
                # Convertir imagen a bytes
                img = Image.open(msg)
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG')
                image_bytes = buffer.getvalue()
                
                # Enviar tamaño del archivo
                file_size = str(len(image_bytes)).encode(FORMAT)
                client.send(file_size)
                
                # Enviar archivo
                client.sendall(image_bytes)
                
                server_msj = client.recv(2048).decode(FORMAT)
                print(server_msj)
                
                if server_msj == 'Disconnect capacity':
                    print("Usted ha sido desconectado, hay mucha gente. Espere un rato y vuelva a intentarlo")
                    client.close()
                    break
                elif server_msj == 'Disconnect':
                    print('Nos vemos, adios!')
                    client.close()
                    break
                
                print(server_msj)
        except ConnectionRefusedError as e:
            print(f"Error de conexión rechazada: {str(e)}")
            print(f"Intentando conectar a {ADDR}")
        except socket.timeout:
            print("La conexión ha expirado. Verifique si el servidor está funcionando.")
        finally:
            client.close()
    else:
        print("Acceso denegado")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--x', type=int, default=8080, help='Numero de puerto')
    parser.add_argument('--z', type=str, default='utf-8', help='Formato de codificación')
    args = parser.parse_args()
    main(args)

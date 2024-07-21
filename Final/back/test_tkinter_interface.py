import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
import io

# Configuración de la interfaz de Tkinter
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Clasificador de Imágenes")

        self.upload_button = tk.Button(root, text="Subir Imagen", command=self.upload_image)
        self.upload_button.pack(pady=20)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.result_label = tk.Label(root, text="Resultado: ")
        self.result_label.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.display_image(file_path)
            self.send_image_for_classification(file_path)

    def display_image(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo

    def send_image_for_classification(self, file_path):
        with open(file_path, 'rb') as file:
            files = {'file': file}
            response = requests.post('http://localhost:5000/upload', files=files)
            if response.status_code == 202:
                task_id = response.json().get('task_id')
                self.check_task_status(task_id)
            else:
                messagebox.showerror("Error", "No se pudo subir la imagen.")

    def check_task_status(self, task_id):
        response = requests.get(f'http://localhost:5000/result/{task_id}')
        if response.status_code == 200:
            result = response.json()
            if result['state'] == 'SUCCESS':
                messagebox.showinfo("Resultado", f"El modelo identificó: {result['result']}")
                self.result_label.config(text=f"Resultado: {result['result']}")
            else:
                self.result_label.config(text="Estado de la tarea: " + result['state'])
        else:
            messagebox.showerror("Error", "No se pudo obtener el resultado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

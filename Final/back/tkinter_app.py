import tkinter as tk
from tkinter import filedialog, messagebox
import requests

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        file_label.config(text=file_path)
    else:
        file_label.config(text="No se ha seleccionado un archivo")

def upload_file():
    file_path = file_label.cget("text")
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
                check_result(task_id)
            else:
                messagebox.showerror("Error", "No se pudo obtener el ID de la tarea")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

def check_result(task_id):
    url = f'http://localhost:5000/result/{task_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        if result['state'] == 'PENDING':
            root.after(2000, check_result, task_id)  # Verifica el estado cada 2 segundos
        else:
            messagebox.showinfo("Resultado", f"Resultado de la Clasificación: {result.get('result', 'Desconocido')}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo obtener el resultado: {e}")

# Configuración de la interfaz de Tkinter
root = tk.Tk()
root.title("Gluten-Free Food Detector")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

file_label = tk.Label(frame, text="No se ha seleccionado un archivo", width=50)
file_label.pack(pady=(0, 10))

select_button = tk.Button(frame, text="Seleccionar archivo", command=select_file)
select_button.pack(side=tk.LEFT, padx=(0, 10))

upload_button = tk.Button(frame, text="Subir y Clasificar", command=upload_file)
upload_button.pack(side=tk.RIGHT)

root.mainloop()

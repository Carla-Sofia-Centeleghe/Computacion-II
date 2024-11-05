import multiprocessing      # Importamos la librería multiprocessing, que sirve para crear procesos
import json                 # Importamos la librería json para leer el archivo de usuarios

class LoginProcess(multiprocessing.Process):   # Creamos una clase LoginProcess que hereda de multiprocessing.Process

    def __init__(self):
        multiprocessing.Process.__init__(self)

    def run(self,usuario,contraseña):
        
        with open('usuario.json') as users:        # Abrimos el archivo de usuarios
            data = json.load(users)                 # Cargamos los usuarios en la variable data
            for clave, valor in data.items():
                if clave == usuario and valor == contraseña:  # Comparamos si el usuario y contraseña son correctos
                    return True
            return False
        
process_log=LoginProcess()          # Creamos un objeto de la clase LoginProcess para poder ejecutar el proceso

def main_log_process(usuario,contraseña):
    return process_log.run(usuario,contraseña) # Ejecutamos el proceso de login
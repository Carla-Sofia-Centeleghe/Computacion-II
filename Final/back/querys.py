import sqlite3  # Importamos la librería para trabajar con SQLite para la base de datos
import datetime # Importamos la librería para trabajar con fechas y horas
import pytz    # Importamos la librería para trabajar con zonas horarias

def consulta(data):

    timezone = pytz.timezone('America/Argentina/Buenos_Aires') # Zona horaria de Buenos Aires
    hora_actual = datetime.datetime.now(timezone)               # Obtenemos la hora actual
    hora_formateada = hora_actual.strftime("%Y-%m-%d %H:%M:%S %Z%z") # Formateamos la hora
    conexion = sqlite3.connect('connections.db')  # Conectamos a la base de datos existente
    cursor = conexion.cursor()
    # Creamos la tabla si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS conexiones ( 
                        id_con INTEGER,
                        hora_actual TEXT
                    )''')

    # Insertamos los datos en la tabla
    cursor.execute("INSERT INTO conexiones (id_con, hora_actual) VALUES (?, ?)", (data, hora_formateada))
    conexion.commit()       # Guardamos los cambios
    conexion.close()        # Cerramos la conexión
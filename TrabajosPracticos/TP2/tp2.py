# Carla Sofia Centeleghe 2023
# Computacion II
# Debo hacer el punto A

import argparse
import os
import threading
import socket
import cv2
from multiprocessing import Process, Pipe
from PIL import Image

def procesar_imagen(archivo_entrada, archivo_salida):
    """
     Proceso una imagen convirtiéndola a escala de grises.

    Parameters:
    - archivo_entrada (str): Ruta del archivo de entrada.
    - archivo_salida (str): Ruta del archivo de salida (imagen en escala de grises).
    """
    try:
        # Cargo la imagen y convierto a escala de grises
        imagen = cv2.imread(archivo_entrada, cv2.IMREAD_COLOR)
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

        # Guardo la imagen procesada
        cv2.imwrite(archivo_salida, imagen_gris)

    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")

def manejar_cliente(socket_cliente, archivo_imagen, socket_servidor):
    """
    Manejo la conexión con un cliente, proceso la imagen y envio la imagen procesada de vuelta.

    Parameters:
    - socket_cliente: Socket de cliente.
    - archivo_imagen (str): Nombre del archivo de imagen a procesar.
    - socket_servidor: Socket del servidor que escucha conexiones.
    """
    try:
        # Proceso la imagen
        archivo_salida = 'gris_' + archivo_imagen
        procesar_imagen(archivo_imagen, archivo_salida)

        # Envio la imagen procesada de vuelta al cliente
        with open(archivo_salida, 'rb') as f:
            socket_cliente.sendall(f.read())

    except Exception as e:
        print(f"Error al manejar al cliente: {str(e)}")

    finally:
        # Cierro el socket del cliente
        socket_cliente.close()

def procesar_imagen_con_pipe(image_path, conn):
    """
    Proceso una imagen convirtiéndola a escala de grises y envio el nombre del archivo procesado a través del Pipe.

    Parameters:
    - image_path (str): Ruta del archivo de imagen de entrada.
    - conn: Objeto de conexión de Pipe.
    """
    try:
        with Image.open(image_path) as img:
            # Convierto la imagen a escala de grises
            converted_img = img.convert('L')
            grayscale_image_path = "gris_" + os.path.basename(image_path)
            converted_img.save(grayscale_image_path)

            # Envio el nombre del archivo procesado a través del Pipe
            conn.send(grayscale_image_path)

    except Exception as e:
        print(f"Error al procesar la imagen con Pipe: {str(e)}")

def servidor(ip, puerto, archivo_imagen):
    """
    Creo un servidor que escucha conexiones y maneja clientes en hilos.

    Parameters:
    - ip (str): Dirección IP para el servidor.
    - puerto (int): Número de puerto para el servidor.
    - archivo_imagen (str): Nombre del archivo de imagen a procesar.
    """
    # Creo un socket que admite tanto IPv4 como IPv6
    socket_servidor = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    try:
        # Intento vincular a IPv6
        socket_servidor.bind((ip, puerto))
    except socket.error:
        # Si fallo, intento vincular a IPv4
        socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_servidor.bind((ip, puerto))

    # Dejo el servidor escuchando
    socket_servidor.listen(1)
    print(f"Escuchando en {ip}:{puerto}")

    while True:
        # Acepto la conexión del cliente
        socket_cliente, direccion = socket_servidor.accept()
        print(f"Conexión aceptada desde {direccion[0]}:{direccion[1]}")

        # Creo un hilo para manejar al cliente
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(socket_cliente, archivo_imagen, socket_servidor))
        hilo_cliente.start()

        # Cierro el socket del servidor después de manejar un cliente
        break

def main():
    """
    Función principal para ejecutar el servidor.
    """
    parser = argparse.ArgumentParser(description='Servidor HTTP y de procesamiento de imágenes en escala de grises')
    parser.add_argument('-i', '--ip', required=True, help='Dirección IP para el servidor')
    parser.add_argument('-p', '--puerto', type=int, required=True, help='Número de puerto para el servidor')
    parser.add_argument('-f', '--archivo', required=True, help='Nombre del archivo de imagen a procesar')
    args = parser.parse_args()

    # Conversión de imágenes
    parent_conn, child_conn = Pipe()
    proceso_conversor = Process(target=procesar_imagen_con_pipe, args=(args.archivo, child_conn))
    proceso_conversor.start()

    try:
        # Espero a que finalice el proceso de conversión de imágenes
        grayscale_image_path = parent_conn.recv()
        proceso_conversor.join()

        # Inicio el servidor para procesar la imagen y espero a que finalice
        servidor(args.ip, args.puerto, grayscale_image_path)

    except KeyboardInterrupt:
        print('Servidor detenido.')

if __name__ == '__main__':
    main()

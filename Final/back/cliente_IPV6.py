import socket       # Importamos el módulo socket para manejar la conexión
import argparse     # Importamos el módulo argparse para manejar argumentos de línea de comandos
from multiprocessing import Queue   # Importamos la clase Queue del módulo multiprocessing para manejar colas
from autentificacion import main_log_process 

def main(args):
    usuarios_queue=Queue()        # Creamos una cola para los usuarios
    contraseñas_queue=Queue()    # Creamos una cola para las contraseñas

    def login():
        usuario=input("Usuario: ")
        contraseña=input("Clave: ")

        usuarios_queue.put(usuario)
        contraseñas_queue.put(contraseña)
    
        log=main_log_process(usuarios_queue.get(),contraseñas_queue.get()) # Llamamos a la función main_log_process del módulo autentificacion para verificar el usuario y la contraseña
        return log
    
    access=login()  

    if access:
        print("Logeo exitoso!")
        HEADER=64
        PORT=args.x
        FORMAT=args.z
        ADDR=('::1',PORT)                               # Creamos una tupla con la dirección IP y el puerto
        CONNECTED=True
        client=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)  # Creamos un socket para la conexión
        client.connect(ADDR)

        while CONNECTED:
            
            def send(msg):                                  # Función para enviar mensajes al servidor
                message=msg.encode(FORMAT)                  # Codificamos el mensaje
                msg_length=len(message)                     # Obtenemos la longitud del mensaje
                send_length=str(msg_length).encode(FORMAT)  # Codificamos la longitud del mensaje
                send_length += b' '*(HEADER-len(send_length)) # Añadimos espacios en blanco para completar el tamaño del encabezado
                client.send(send_length)                      # Enviamos la longitud del mensaje
                client.send(message)                          # Enviamos el mensaje
                server_msj=client.recv(2048).decode(FORMAT)   # Recibimos la respuesta del servidor
                return server_msj                             # Retornamos la respuesta del servidor
            
            if True:
                msg=input("detector de comida")

                server_msj=send(msg)

                if server_msj=='Disconnect capacity':
                    print("Usted ha sido desconectado, hay mucha gente. Espere un rato y vuelva a intentarlo")
                    client.close()
                    break
                if server_msj=='Disconnect':
                    print('Nos vemos, adios!')
                    client.close()
                    break
                
                print(server_msj)
            
            print(server_msj)
    else:
        print("Acceso denegado")
if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--x',type=int,default=8080,help='Numero de puerto')    # Argumento para el número de puerto
    parser.add_argument('--z',type=str,default='utf-8',help='Formato de codificacion')  # Argumento para el formato de codificación
    args=parser.parse_args() # Parseamos los argumentos para obtener los valores
    main(args)
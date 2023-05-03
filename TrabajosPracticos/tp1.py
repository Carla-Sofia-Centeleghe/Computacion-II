##--------------------------------- Carla Sofia Centeleghe 20223----------------------------------------------------------------
#-----------------TRABAJO PRACTICO N° 1 ----------------------------------------------------------------------------------------

#importo las librerias
import argparse
import os

def InvertirLineas(linea):
    return linea.strip()[::-1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", action = "store", required = True, type = str, help = "el archivo a leer")
    args = parser.parse_args()

    file = args.file
    pid = os.fork ()
    r, w = os.pipe()
    pipes = []
    imprimir = []

    try:
        with open(file, 'r') as f: # Leer las líneas del archivo
            lineas = f.readlines()

        for linea in lineas:
            
            if pid != 0:
                os.close(w)
                pipes.append(r)

                os.waitpid(pid, 0)
            else: 
                os.close(r)
                w = os.read(pipe, 1024)
                os.write(w,(InvertirLineas(linea)).encode())
                os.close(w)
                exit(0)
        
       
        for pipe in pipes:
            r = os.read(pipe, 1024)
            data_d = r.readlines().decode().strip()
            imprimir.append(data_d)
            r.close()

    except IOError:
            print(f"No se puede abrir el archivo {args.file}")
            exit()

    for data_d in imprimir:
        print(data_d)
        print("\n")

if __name__ == "__main__":
    main()

        
#1- Escribir un programa en Python que acepte un número de argumento entero positivo n y genere una lista de los n primeros números impares. 
# El programa debe imprimir la lista resultante en la salida estandar.
#!/bin/bash python3 

import argparse


def main():
    parser = argparse.ArgumentParser(description='Ingresa numeros') 
    parser.add_argument('-n', type=int, help='Ingresa valores positivo') 
    args = parser.parse_args() 

    
    if args.n <=0:
        raise ValueError('n debe ser un número entero positivo')
    else:
        impares = []
        for i in range(1, 2*args.n, 2):
            impares.append(i)
        print(impares)

if __name__=='__main__':
    main()


   
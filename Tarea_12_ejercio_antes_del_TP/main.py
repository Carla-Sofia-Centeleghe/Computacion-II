# Grupo Carla S. Centeleghe y Cristian Albornoz
# 1 hilo para main, 1 hilo sumatorio y tantos hilos como teerminos

import math
import threading as th

def taylor_serie(n, x):
    global taylor_list
    taylor_list.append(((-1)**n/math.factorial(2*n+1))*x**(float(2*n+1)))

def threading_manager():
    for i in range(numbers):
        th1 = th.Thread(target= taylor_serie, args=(numbers,x))
        th1.start()
        th_l.append(th1)

    for i in th_l:
        th1.join()

def suma():
    global taylor_list
    global sums
    sums = 0
    for i in taylor_list:
        sums += i

if __name__ =='__main__':
    taylor_list = []
    sums = 0
    numbers = int(input('Give number of terms: '))
    x = float(input('Give the x value: '))
    th_l =[]

    threading_manager()

    th2 = th.Thread(target=suma)
    th2.start()
    th2.join()

    print(f'The umber of is terms: {numbers}')
    print(f'X = {sums}')
    print(f'Reference value: {math.sin(x)}')
    print(f'Error: {abs(sums-math.sin(x))}')

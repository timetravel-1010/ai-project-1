import pygame as pg
import sys, os
import time
import numpy as np

from juego.robot import Robot

from algoritmos.preferencia_amplitud import preferencia_amplitud
from algoritmos.costo_uniforme import costo_uniforme
from algoritmos.preferente_profundidad import preferente_profundidad
from algoritmos.avara import avara
from algoritmos.algoritmo_estrella import estrella

n = 10 #matriz nxn
nombre_lectura = "mundo" #nombre del archivo txt sin .txt
ancho = 640 #ancho de la pantalla
alto = ancho
size = ancho // n #tamaño del lado de cada cuadrado
x0 = 0
y0 = 0
ticks = 3 #velocidad del reloj, mayor valor -> mayor velocidad.

colores = { 0:(255,255,255), # 0 -> casilla libre
            1:(150,75,0),
            -1:(255,255,255), # 1 -> muro
            2:(0,230,230),
            -2:(0,230,230), # 2 -> punto de inicio
            3:(0, 255, 0),
            #-3:(0, 255, 0), # 3 -> nave1
            4:(204,204,255),
            #-4:(204,204,255), # 4 -> nave2
            5:(255,255,0),
            #-5:(255,255,0), # 5 -> item 
            6:(255,0,0),
            -6:(255,0,0) } # 6 -> aceite
'''
input: lee el archivo .txt y carga el mundo en un array de numpy y
encuentra y establece la posición inicial del robot (x0, y0).
''' 
pos_item1 = {'x': 0, 'y': 0}
pos_item2 = {'x': 0, 'y': 0}

def game(algoritmo): 

    def input():
        global x0, y0, pos_item1, pos_item2
        items_encontrados = 0

        with open(f"mundos/{nombre_lectura}.txt", "r") as f:
            content = f.read().split('\n')
            mundo = []
            for i in range(n):
                fila = list(map(lambda x: int(x), content[i].split(" ")))
                mundo.append(fila)
                try: 
                    y0 = fila.index(2)
                    x0 = i  
                except ValueError:
                    pass 
                try:
                    if items_encontrados == 0:
                        y = fila.index(5)
                        pos_item1['y'] = y  # [0 1 1 1 1 0 1 1 1 5]-> 9
                        pos_item1['x'] = i
                        items_encontrados += 1 
                        try: 
                            pos_item2['y'] = fila.index(5, y+1) # [0 1 1 1 1 0 1 1 1 5]-> 9
                            pos_item2['x'] = i
                            items_encontrados += 1
                        except ValueError:
                            pass 
                    elif items_encontrados == 1:
                        pos_item2['y'] = fila.index(5) # [0 1 1 1 1 0 1 1 1 5]-> 9
                        pos_item2['x'] = i
                        items_encontrados += 1  
                except ValueError:
                    pass
            return np.array(mundo)

    #configuración inicial de la pantalla
    def setup():
        global pantalla 
        pg.init()
        pantalla = pg.display.set_mode((ancho, alto))
        pg.display.set_caption('Smart Robot')
        pantalla.fill((255,255,255)) 

    """ crear la cuadrícula """
    def grid():
        x = 0
        y = 0
        limite_horizontal = alto
        limite_vertical = ancho
        for l in range(n+1):
            pg.draw.line(pantalla, (0,0,0), (x,0), (x, limite_horizontal))
            pg.draw.line(pantalla, (0,0,0), (0,y), (limite_vertical, y))
            x += size
            y += size
    '''
    pintar_mundo: recorrre la matriz del mundo y pinta los cuadros correspondientes
    al elemento que se encuentra en cada celda.
    '''
    def pintar_mundo(mundo):
        x = 0
        y = 0
        tam = size #tamaño de cada cuadro.
        for fila in mundo: #recorre las filas.
            for valor in fila: #recorre cada elemento de la fila.
                pg.draw.rect(pantalla, pg.__color_constructor(colores.get(valor)[0], #se pinta el cuadro dependiendo el número que tiene.
                                                            colores.get(valor)[1], 
                                                            colores.get(valor)[2], 
                                                            0), 
                                                            (x, y, tam, tam)) #posicion x, posicion y, ancho, alto.           
                x += tam
            x = 0
            y += tam

    # bucle infinito para mostrar en patalla todos los elementos gráficos.
    def mostrar_juego(valores): # resultado = [nodo5, nodo4, nodo3, nodo2, nodo1]
        resultado = valores[0]
        #print("resultado. ", resultado)
        i = len(resultado)-1 #para recorrer la lista (resultado) de atrás hacia adelante
        
        while True:
            clock.tick(ticks) 

            for event in pg.event.get():
                if event.type == pg.QUIT: #para detener la ejecución al cerrar la ventana
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        pass

            if (i >= 0):            
                try:
                    pintar_mundo(resultado[i][1]) #pinta el mundo correspondiente al nodo actual.
                    robot.mover(resultado[i][0]) #se obtiene el operador para mover el robot. 
                    #print("combustible actual:", resultado[i][2])
                    #print("costo: ", resultado[i][3])
                    #print("heuristica: ", resultado[i][4])
                    robot.pintar()
                except ValueError:
                    print("No se encontró la solución.")

            grid() #mostrar la cuadrícula.
            i -= 1 
            pg.display.update()
            pg.display.flip() #actualizar el mundo para mostrar nuevos cambios.

    # Inicio
    setup() #pantalla
    mundo = input() #se carga la matriz del mundo.
    robot = Robot(x0*size, y0*size,(100,100,230), size, pantalla) #se crea el robot.
    clock = pg.time.Clock() #reloj para manipular la velocidad de la ejecución.

    #se muestra por primera vez el mundo
    pintar_mundo(mundo)
    robot.pintar()
    grid()
    pg.display.flip()
    if algoritmo == "amplitud":
        resultado = preferencia_amplitud(mundo, x0, y0)
    elif algoritmo == "costo":
        resultado = costo_uniforme(mundo, x0, y0)
    elif algoritmo == "profundidad":
        resultado = preferente_profundidad(mundo, x0, y0)
    elif algoritmo == "avara":
        resultado = avara(mundo, x0, y0, pos_item1, pos_item2)
    elif algoritmo == "estrella":
        resultado = estrella(mundo, x0, y0, pos_item1, pos_item2)

    print(resultado)
    mostrar_juego(resultado) #mostrar el juego en pantalla.

game("profundidad")
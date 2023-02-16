import pygame as pg
import sys
import os
import numpy as np
import time

from juego.robot import Robot
from juego.button import Button

from algoritmos.preferencia_amplitud import preferencia_amplitud
from algoritmos.costo_uniforme import costo_uniforme
from algoritmos.preferente_profundidad import preferente_profundidad
from algoritmos.avara import avara
from algoritmos.algoritmo_estrella import estrella

pg.init()
WIDTH = 640 #ancho
EXTRA_WIDTH = 400 # espacio extra en el ancho para el panel derecho.
TOTAL_WIDTH = WIDTH+EXTRA_WIDTH
HEIGHT = WIDTH # alto
os.environ['SDL_VIDEO_CENTERED'] = '1'
SCREEN = pg.display.set_mode((TOTAL_WIDTH, HEIGHT))
pg.display.set_caption("Menu")

BG = pg.image.load("juego/assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pg.font.Font("juego/assets/font.ttf", size)

# =================================== Mundo ========================= #
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
            -3:(0, 255, 0), # 3 -> nave1
            4:(204,204,255),
            -4:(204,204,255), # 4 -> nave2
            5:(255,255,0),
            -5:(255,255,0), # 5 -> item 
            6:(255,0,0),
            -6:(255,0,0) } # 6 -> aceite
'''
input: lee el archivo .txt y carga el mundo en un array de numpy y
encuentra y establece la posición inicial del robot (x0, y0).
''' 
pos_item1 = {'x': 0, 'y': 0}
pos_item2 = {'x': 0, 'y': 0}

def game(SCREEN, algoritmo): 
    pantalla = SCREEN

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
        #global pantalla 
        pg.init()
        #pantalla = pg.display.set_mode((ancho, alto))#+200
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
        # valores = [camino, nodos_expandidos, profundidad, tiempo, costo]
        resultado = valores[0]
        i = len(resultado)-1 #para recorrer la lista (resultado) de atrás hacia adelante
       
        while True:

            NODOS_EXPANDIDOS = get_font(13).render(f"nodos expandidos: {valores[1]}", True, "Black")
            NODOS_RECT = NODOS_EXPANDIDOS.get_rect(center=(790, 200))

            PROFUNDIDAD = get_font(13).render(f"profunidad: {valores[2]}", True, "Black")
            PROFUNDIDAD_RECT = NODOS_EXPANDIDOS.get_rect(center=(790, 250))

            TIEMPO = get_font(13).render(f"tiempo: {valores[3]}", True, "Black")
            TIEMPO_RECT = NODOS_EXPANDIDOS.get_rect(center=(790, 300))

            COSTO = get_font(13).render(f"costo: {valores[4]}", True, "Black")
            COSTO_RECT = NODOS_EXPANDIDOS.get_rect(center=(790, 350))

            OPTIONS_MOUSE_POS = pg.mouse.get_pos()
            clock.tick(ticks) 
            VOLVER = Button(image=None, pos=(740, 460), 
                            text_input="REGRESAR", font=get_font(15), base_color="Black", hovering_color="Green")
            VOLVER.changeColor(OPTIONS_MOUSE_POS)
            VOLVER.update(SCREEN)
            SCREEN.blit(NODOS_EXPANDIDOS, NODOS_RECT)
            SCREEN.blit(PROFUNDIDAD, PROFUNDIDAD_RECT)
            SCREEN.blit(TIEMPO, TIEMPO_RECT) 
            SCREEN.blit(COSTO, COSTO_RECT)
            
            for event in pg.event.get():
                if event.type == pg.QUIT: #para detener la ejecución al cerrar la ventana
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if VOLVER.checkForInput(OPTIONS_MOUSE_POS):
                        main_menu()

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
    # resultado = [camino, nodos_expandidos, profundidad, tiempo, costo]
    if algoritmo == "amplitud":
        resultado = preferencia_amplitud(mundo, x0, y0)
        #resultado, nodos_expandidos, profundidad, tiempo, costo = preferencia_amplitud(mundo, x0, y0)
    elif algoritmo == "costo":
        resultado = costo_uniforme(mundo, x0, y0)
        #resultado, nodos_expandidos, profundidad, tiempo, costo = costo_uniforme(mundo, x0, y0)
    elif algoritmo == "profundidad":
        resultado = preferente_profundidad(mundo, x0, y0)
        #resultado, nodos_expandidos, profundidad, tiempo, costo = preferente_profundidad(mundo, x0, y0)
    elif algoritmo == "avara":
        resultado = avara(mundo, x0, y0, pos_item1, pos_item2)
        #resultado, nodos_expandidos, profundidad, tiempo, costo = avara(mundo, x0, y0, pos_item1, pos_item2)
    elif algoritmo == "estrella":
        resultado = estrella(mundo, x0, y0, pos_item1, pos_item2)
        #resultado, nodos_expandidos, profundidad, tiempo, costo = estrella(mundo, x0, y0, pos_item1, pos_item2)
    movimientos = [x[0] for x in resultado[0]]
    movimientos.reverse()
    print("movimientos:", movimientos)
    mostrar_juego(resultado) #mostrar el juego en pantalla.

# ================================= Opciones =========================

def busqueda_informada():
    while True:
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()
        SCREEN.fill("white")

        AVARA = Button(image=None, pos=(TOTAL_WIDTH/2, 160), 
                            text_input="AVARA", font=get_font(35), base_color="Black", hovering_color="Green")
        AVARA.changeColor(OPTIONS_MOUSE_POS)
        AVARA.update(SCREEN)

        A_ESTRELLA = Button(image=None, pos=(TOTAL_WIDTH/2, 260), 
                            text_input="A*", font=get_font(35), base_color="Black", hovering_color="Green")
        A_ESTRELLA.changeColor(OPTIONS_MOUSE_POS)
        A_ESTRELLA.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=(TOTAL_WIDTH/2, 560), 
                            text_input="REGRESAR", font=get_font(35), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                elif AVARA.checkForInput(OPTIONS_MOUSE_POS):
                    game(SCREEN, "avara")
                elif A_ESTRELLA.checkForInput(OPTIONS_MOUSE_POS):
                    game(SCREEN, "estrella")

        pg.display.update()
    
def busqueda_no_informada():
    while True:
        OPTIONS_MOUSE_POS = pg.mouse.get_pos()
        SCREEN.fill("white")

        AMPLITUD = Button(image=None, pos=(TOTAL_WIDTH/2, 160), 
                            text_input="AMPLITUD", font=get_font(35), base_color="Black", hovering_color="Green")
        AMPLITUD.changeColor(OPTIONS_MOUSE_POS)
        AMPLITUD.update(SCREEN)

        COSTO_UNIFORME = Button(image=None, pos=(TOTAL_WIDTH/2, 260), 
                            text_input="COSTO UNIFORME", font=get_font(35), base_color="Black", hovering_color="Green")
        COSTO_UNIFORME.changeColor(OPTIONS_MOUSE_POS)
        COSTO_UNIFORME.update(SCREEN)

        PROFUNDIDAD_EVITANDO_CICLOS = Button(image=None, pos=(TOTAL_WIDTH/2, 360), 
                            text_input="PROFUNDIDAD EVITANDO CICLOS", font=get_font(30), base_color="Black", hovering_color="Green")
        PROFUNDIDAD_EVITANDO_CICLOS.changeColor(OPTIONS_MOUSE_POS)
        PROFUNDIDAD_EVITANDO_CICLOS.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=(TOTAL_WIDTH/2, 560), 
                            text_input="REGRESAR", font=get_font(35), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                elif AMPLITUD.checkForInput(OPTIONS_MOUSE_POS):
                    game(SCREEN, "amplitud")
                elif COSTO_UNIFORME.checkForInput(OPTIONS_MOUSE_POS):
                    game(SCREEN, "costo")
                elif PROFUNDIDAD_EVITANDO_CICLOS.checkForInput(OPTIONS_MOUSE_POS):
                    game(SCREEN, "profundidad")

        pg.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pg.mouse.get_pos()

        MENU_TEXT = get_font(70).render("SMART ROBOT", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(TOTAL_WIDTH/2, 100))

        PLAY_BUTTON = Button(image=None,#image=pg.image.load("juego/assets/Play Rect.png"), 
        pos=(TOTAL_WIDTH/2, 250), 
                            text_input="BÚSQUEDA INFORMADA", font=get_font(30), base_color="White", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=None,#image=pg.image.load("juego/assets/Options Rect.png"), 
        pos=(TOTAL_WIDTH/2, 350), 
                            text_input="BÚSQUEDA NO INFORMADA", font=get_font(30), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=None,#image=pg.image.load("juego/assets/Quit Rect.png"), 
        pos=(TOTAL_WIDTH/2, 450), 
                            text_input="SALIR", font=get_font(35), base_color="White", hovering_color="Green")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    busqueda_informada()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    busqueda_no_informada()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.quit()
                    sys.exit()

        pg.display.update()

main_menu()
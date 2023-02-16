from algoritmos.nodo import Nodo, operadores
import numpy as np
import time

cola = []
nodos_expandidos = 0

# funcion que implementa el algoritmo de búsqueda preferente por profundidad.
def preferente_profundidad(matriz, x, y):
    start = time.perf_counter()
    global cola, nodos_expandidos, camino, profundidad, costo
        
    nodo_raiz = Nodo(matriz, x, y, None, None, 0, 0, False, 0, 0, matriz)
    cola.append(nodo_raiz)

    while True: 
        if cola == []:
            return "Falla"
        cabeza = cola[0]
        nodos_expandidos += 1
        cola = cola[1:]
        if cabeza.es_meta(): 
            costo = cabeza.costo
            profundidad = cabeza.profundidad
            camino = cabeza.encontrar_camino() 
            print("nodos expandidos: ", nodos_expandidos)
            print("profundidad: ", profundidad)
            print("costo:", costo)
            break
        crear_hijos(cabeza)         
    end = time.perf_counter()
    tiempo = end-start
    print("tiempo en algoritmo: ", tiempo)
    return [camino, nodos_expandidos, profundidad, tiempo, costo]   

def crear_hijos(nodo_padre):

    global cola
    nave_hijo = nodo_padre.validar_nave()
    nuevo_combustible = nodo_padre.combustible-1 if nave_hijo else 0

    matriz_copia = nodo_padre.matriz.copy()
    x = nodo_padre.x
    y = nodo_padre.y

    aux_profundidad = nodo_padre.profundidad + 1 
    matriz_copia = validar_cambio_matriz(nodo_padre, matriz_copia, x, y).copy()
    matriz_copia = restringir_camino(matriz_copia, x, y).copy()
    costo_padre = nodo_padre.costo

    valores_casillas = { "arriba": nodo_padre.estado["arriba"], 
                         "abajo": nodo_padre.estado["abajo"], 
                         "izquierda": nodo_padre.estado["izquierda"], 
                         "derecha": nodo_padre.estado["derecha"] }
    
    opuesto_de = { "arriba":"abajo", "abajo":"arriba", "izquierda":"derecha", "derecha":"izquierda" }
    tipo_nave_diferentes = False

    nuevas_posiciones = { "arriba": [x-1, y], "abajo": [x+1, y], "izquierda": [x, y-1], "derecha": [x, y+1] }


    for i in range(len(operadores)-1, -1, -1):


        casilla_siguiente = valores_casillas[operadores[i]] # guarda el valor de la casilla siguiente (en la que está cada hijo).
        
        if (casilla_siguiente >= 0 and casilla_siguiente != 1):
            se_devuelve = nodo_padre.operador == opuesto_de[operadores[i]]
            if (nodo_padre.nodo_padre):
                tipo_nave_diferentes = nodo_padre.nave != nave_hijo
                casilla_siguiente_nave = False
                if not nave_hijo:
                    casilla_siguiente_nave = nodo_padre.nave != (casilla_siguiente == 3 or casilla_siguiente == 4)

            if ( (se_devuelve and ( tipo_nave_diferentes or nodo_padre.item_encontrado or casilla_siguiente_nave)) or not se_devuelve):

                nuevo_x = nuevas_posiciones[operadores[i]][0] # 0 -> x
                nuevo_y = nuevas_posiciones[operadores[i]][1] # 1 -> y

                new_nodo = Nodo(matriz_copia, nuevo_x, nuevo_y, nodo_padre, operadores[i], aux_profundidad, costo_padre, nave_hijo, nuevo_combustible, nodo_padre.cantidad_item, nodo_padre.matriz_aux)
                new_nodo.actualizar_estado_casilla()
                cola.insert(0, new_nodo)

def validar_cambio_matriz(nodo_padre, matriz, x, y):
    """ Se valida si es necesario hacer un cambio a la matriz,
        dependiendo si se encontró con una nave o un item,
        si uno de estos casos se cumple se cambia a la matriz inicial, 
        pero quitando el item o la nave que se encuentre en la posición inicial. """

    try:
        # print(nodo_padre.item_encontrado)
        if (nodo_padre.combustible == 21) or (nodo_padre.combustible == 11 and nodo_padre.nodo_padre.combustible != 12) or nodo_padre.item_encontrado:
            nodo_padre.matriz_aux[x][y] = 0
            nodo_padre.matriz = np.array(nodo_padre.matriz_aux)
            nodo_padre.estado = nodo_padre.validar_direcciones(x, y)

            return nodo_padre.matriz_aux
    except AttributeError:
        return matriz
    else: 
        return matriz


def restringir_camino(matriz, x, y):
    """ Restringe el camino por donde pasa, para evitar entrar en un ciclo. """
    if abs(matriz[x][y]) == 6:
        matriz[x][y] = -6
    elif abs(matriz[x][y]) == 2:
        matriz[x][y] = -2
    else:
        matriz[x][y] = -1
    return matriz 
from algoritmos.nodo import Nodo, operadores
import queue
import time

cola_prioridad = queue.PriorityQueue() # importante tener cuidado con el límite 
nodos_expandidos = 0
contador = 0
pos_item1 = {}
pos_item2 = {}
distancia_items = 0  

# funcion que implementa el algoritmo de búsqueda preferente por amplitud.
def estrella(matriz, x, y, posItem1, posItem2):
    start = time.perf_counter()
    global cola_prioridad, nodos_expandidos, pos_item1, pos_item2, distancia_items, profundidad, costo, camino

    pos_item1 = posItem1
    pos_item2 = posItem2

    nodo_raiz = Nodo(matriz, x, y, None, None, 0, 0, False, 0, 0)
    cola_prioridad.put(nodo_raiz)

    distancia_items = manhattan(pos_item1["x"], pos_item1["y"], pos_item2["x"], pos_item2["y"])

    while True: 
        if cola_prioridad.empty():
            print("No se ha encontrado el camino.")
            exit(-1)
            return "Falla"
        cabeza = cola_prioridad.get()
        nodos_expandidos += 1
        
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

# función que calcula la distancia de manhattan de un nodo con respecto a un ítem.
def manhattan(x1, y1, x2, y2): # nodo, pos_item
    # resultado = abs(nodo.x - pos_item['posx']) + abs(nodo.y - pos_item['posy'])
    resultado = abs(x2 - x1) + abs(y2 - y1)
    return resultado

def calcular_heuristica(nodo):
    #global nodo.buscar_item1, nodo.buscar_item2, distancia_items
    #  min(mh(agente, item1) + mh(item1, item2), mh(agente, item2) + mh(item1, item2))

    
    if nodo.buscar_item2 and not nodo.buscar_item1: # solo busca el item2 (ya encontró el 1).
        manhattan_item = manhattan(nodo.x, nodo.y, pos_item2["x"], pos_item2['y'])
        distancia_total = manhattan_item
    elif nodo.buscar_item1 and not nodo.buscar_item2: # solo busca el item1 (ya encontró el 2).
        manhattan_item = manhattan(nodo.x, nodo.y, pos_item1["x"], pos_item1['y'])
        distancia_total = manhattan_item
    elif nodo.buscar_item1 and nodo.buscar_item2:
        manhattan_item1 = manhattan(nodo.x, nodo.y, pos_item1["x"], pos_item1['y'])
        manhattan_item2 = manhattan(nodo.x, nodo.y, pos_item2["x"], pos_item2['y'])
        if manhattan_item1 == 0:
            nodo.buscar_item1 = False
        elif manhattan_item2 == 0:
            nodo.buscar_item2 = False

        distancia_total = min(manhattan_item1 , manhattan_item2) + distancia_items  # manhattan_item1 + manhattan_item2 # no ha encontrado ningún ítem
    return distancia_total


def crear_hijos(nodo_padre):
    global contador 
    global cola_prioridad

    contador += 1 

    nave_hijo = nodo_padre.validar_nave()
    nuevo_combustible = nodo_padre.combustible-1 if nave_hijo else 0

    matriz_copia = nodo_padre.matriz.copy()
    x = nodo_padre.x
    y = nodo_padre.y

    valores_casillas = { "arriba": nodo_padre.estado["arriba"], 
                         "abajo": nodo_padre.estado["abajo"], 
                         "izquierda": nodo_padre.estado["izquierda"], 
                         "derecha": nodo_padre.estado["derecha"] }
    
    opuesto_de = { "arriba":"abajo", "abajo":"arriba", "izquierda":"derecha", "derecha":"izquierda" }
    tipo_nave_diferentes = False

    nuevas_posiciones = { "arriba": [x-1, y], "abajo": [x+1, y], "izquierda": [x, y-1], "derecha": [x, y+1] }

    aux_profundidad = nodo_padre.profundidad + 1 
    costo_padre = nodo_padre.costo

    for op_actual in operadores: # ["derecha", "izquierda", etc]
        #contrario = anterior, ej: actual = arriba -> contrario = abajo
        casilla_siguiente = valores_casillas[op_actual] # guarda el valor de la casilla siguiente (en la que está cada hijo).
        
        if (casilla_siguiente != -1 and casilla_siguiente != 1):
            se_devuelve = nodo_padre.operador == opuesto_de[op_actual]
            if (nodo_padre.nodo_padre):
                tipo_nave_diferentes = nodo_padre.nodo_padre.nave != nave_hijo
                casilla_siguiente_nave = False
                if not nave_hijo:
                    casilla_siguiente_nave = nodo_padre.nave != (casilla_siguiente == 3 or casilla_siguiente == 4)

            if ( (se_devuelve and ( tipo_nave_diferentes or nodo_padre.item_encontrado or casilla_siguiente_nave)) or not se_devuelve):

                nuevo_x = nuevas_posiciones[op_actual][0] # 0 -> x
                nuevo_y = nuevas_posiciones[op_actual][1] # 1 -> y

                new_nodo = Nodo(matriz_copia, nuevo_x, nuevo_y, nodo_padre, op_actual, aux_profundidad, costo_padre, nave_hijo, nuevo_combustible, nodo_padre.cantidad_item, buscar_item1=nodo_padre.buscar_item1, buscar_item2=nodo_padre.buscar_item2)
                new_nodo.actualizar_estado_casilla()
                new_nodo.heuristica = calcular_heuristica(new_nodo)
                cola_prioridad.put(new_nodo)
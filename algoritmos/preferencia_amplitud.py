from algoritmos.nodo import Nodo, operadores
import time

cola = []
nodos_expandidos = 0
contador = 0

# funcion que implementa el algoritmo de búsqueda preferente por amplitud.
def preferencia_amplitud(matriz, x, y):
    start = time.perf_counter()
    global cola, nodos_expandidos, profundidad, costo, camino

    nodo_raiz = Nodo(matriz, x, y, None, None, 0, 0, False, 0, 0)
    cola.append(nodo_raiz)
    #print("Soy el nodo raiz con inicio x: ", nodo_raiz.x, ", y: ", nodo_raiz.y)
    while True: 
        if cola == []:
            return "Falla"
        cabeza = cola[0]
        nodos_expandidos = nodos_expandidos + 1
        cola = cola[1:]
        #cabeza.actualizar_estado_casilla()
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
    global cola, contador 

    contador += 1
    nave_hijo = nodo_padre.validar_nave() 
    nuevo_combustible = nodo_padre.combustible-1 if nave_hijo else 0
    
    matriz_copia = nodo_padre.matriz.copy()
    aux_profundidad = nodo_padre.profundidad + 1 
    costo_padre = nodo_padre.costo
    x = nodo_padre.x
    y = nodo_padre.y

    valores_casillas = { "arriba": nodo_padre.estado["arriba"], 
                         "abajo": nodo_padre.estado["abajo"], 
                         "izquierda": nodo_padre.estado["izquierda"], 
                         "derecha": nodo_padre.estado["derecha"] }
    
    opuesto_de = { "arriba":"abajo", "abajo":"arriba", "izquierda":"derecha", "derecha":"izquierda" }
    tipo_nave_diferentes = False

    nuevas_posiciones = { "arriba": [x-1, y], "abajo": [x+1, y], "izquierda": [x, y-1], "derecha": [x, y+1] }

    for op_actual in operadores: # ["derecha", "izquierda", etc]
        #contrario = anterior, ej: actual = arriba -> contrario = abajo
        casilla_siguiente = valores_casillas[op_actual] # guarda el valor de la casilla siguiente (en la que está cada hijo).
        
        if (casilla_siguiente != -1 and casilla_siguiente != 1):
            se_devuelve = nodo_padre.operador == opuesto_de[op_actual]
            if (nodo_padre.nodo_padre):
                tipo_nave_diferentes = nodo_padre.nave != nave_hijo
                casilla_siguiente_nave = False
                if not nave_hijo:
                    casilla_siguiente_nave = nodo_padre.nave != (casilla_siguiente == 3 or casilla_siguiente == 4)

            if ( (se_devuelve and ( tipo_nave_diferentes or nodo_padre.item_encontrado or casilla_siguiente_nave)) or not se_devuelve):

                nuevo_x = nuevas_posiciones[op_actual][0] # 0 -> x
                nuevo_y = nuevas_posiciones[op_actual][1] # 1 -> y

                new_nodo = Nodo(matriz_copia, nuevo_x, nuevo_y, nodo_padre, op_actual, aux_profundidad, costo_padre, nave_hijo, nuevo_combustible, nodo_padre.cantidad_item)
                new_nodo.actualizar_estado_casilla()
                cola.append(new_nodo)
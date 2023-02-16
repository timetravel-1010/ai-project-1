import numpy as np
import functools

total_items = 2
operadores = ["izquierda", "derecha", "arriba", "abajo",]
#operadores = ["derecha", "abajo", "izquierda", "arriba"]
class Nodo:
    
    def __init__(self, matriz, x, y, nodo_padre, operador, profundidad, costo, nave, combustible, cantidad_item, matriz_aux=None, algoritmo_avara=False, buscar_item1=True, buscar_item2=True, count_aux=None) -> None:
        self.matriz = np.array(matriz)
        self.x = x
        self.y = y
        self.nodo_padre = nodo_padre
        self.operador = operador
        self.profundidad = profundidad
        self.costo = costo
        self.heuristica = 0
        self.nave = nave
        self.combustible = combustible
        self.estado = self.validar_direcciones(x, y)
        self.cantidad_item = cantidad_item
        self.item_encontrado = False
        self.matriz_aux = np.array(matriz_aux)
        self.algoritmo_avara = algoritmo_avara
        self.buscar_item1 = buscar_item1
        self.buscar_item2 = buscar_item2
        self.count_aux = count_aux

    #método que comprueba si este nodo es meta, True si es meta, False en caso contrario.
    def es_meta(self) -> bool:
        #print(self.matriz)
        return self.cantidad_item == total_items


    def actualizar_estado_casilla(self) -> None: 
        """
        método para obtener (si corresponde) el elemento que se 
        encuentra en la posición actual del nodo (una nave o un ítem).
        """
        casilla_actual = self.matriz[self.x][self.y]

        if (casilla_actual == 4 or casilla_actual == 3) and not self.nave: #valida si es una nave
            self.combustible = 11 if casilla_actual == 3 else 21
            self.matriz[self.x][self.y] = 0 #una vez obtenida la nave, donde estaba debe haber un 0.
            self.nave = True
        elif casilla_actual == 5: # encuentra el item
            self.matriz[self.x][self.y] = 0 #lo mismo de arriba pero con el ítem.
            self.cantidad_item += 1
            self.item_encontrado = True
        
        # se calcula el costo del movimiento.
        if casilla_actual == 6 and self.combustible == 0:
            self.costo += 4
        else:
            self.costo += 1

        
    #método para saber si el nodo hijo tiene o no nave.
    def validar_nave(self) -> None:
        if self.nave:  
            nuevo_combustible = self.combustible - 1 #combustible del hijo.
            return nuevo_combustible != 0 # True si tiene nave o False en caso contrario
        else:
            return False

    def encontrar_camino(self) -> list:
        '''
        método que retorna una lista con parejas (operador, mundo), correspondientes al camino
        para llegar a la meta y el estado del mundo en cada nodo.
        '''
        #print("combustible actual:", self.combustible)
        if self.nodo_padre is None:
            return []
        else:    
            return [[self.operador, self.matriz, self.combustible, self.costo, self.heuristica]] + self.nodo_padre.encontrar_camino() 


    def encontrar_camino_aux(self) -> list:
        '''
        método que retorna una lista con parejas (operador, mundo), correspondientes al camino
        para llegar a la meta y el estado del mundo en cada nodo.
        '''
        #print("combustible actual:", self.combustible)
        if self.nodo_padre is None:
            return []
        else:    
            return [self.nave, [self.operador]] + self.nodo_padre.encontrar_camino_aux() 
    


    #método que verifica que en cada dirección no se salga de la matriz.
    def validar_direcciones(self, x, y):
        izquierda = self.matriz[self.x][self.y-1] if y > 0 else -1
        derecha = self.matriz[self.x][self.y+1] if y < len(self.matriz)-1 else -1
        arriba = self.matriz[self.x-1][self.y] if x > 0 else -1
        abajo = self.matriz[self.x+1][self.y] if x < len(self.matriz)-1 else -1

        return  {
            "izquierda": izquierda, 
            "derecha": derecha, 
            "arriba": arriba,
            "abajo": abajo,    
        } 

    def __lt__(self, other):
        if self.algoritmo_avara:
            return (self.heuristica < other.heuristica)
        return ((self.heuristica + self.costo) < (other.heuristica + other.costo))
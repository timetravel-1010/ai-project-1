import pygame as pg

#Clase utilizada para mostrar el robot en pantalla.
class Robot():
    def __init__(self, x, y, color, tam, pantalla):
        self.x = y
        self.y = x
        self.color = color
        self.tam = tam
        self.pantalla = pantalla
    
    def pintar(self):
        pg.draw.rect(self.pantalla, #se pinta en pantalla.
                    self.color, #colores del robot
                    (self.x, self.y, self.tam, self.tam)) #posicion x, posicion y, ancho, alto.

    def mover(self, direccion):
        if direccion == "izquierda":
            self.x -= self.tam
        elif direccion == "derecha":
            self.x += self.tam
        elif direccion == "arriba":
            self.y -= self.tam
        elif direccion == "abajo":
            self.y += self.tam
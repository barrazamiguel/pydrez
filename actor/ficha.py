# -*- encoding: utf-8 -*-
from pilasengine.actores.actor import Actor

class Ficha(Actor):

    def iniciar(self, color="blanco", fila=1, columna=1):
        self.imagen = "imagenes/pieza/"+color+"/"+self.nombre()+".png"
        self.color = color
        self.escala = 0.7
        self.columna = columna
        self.fila = fila
        self.tablero = None

    def definirTablero(self, tablero):
        self.tablero = tablero

    def puedeMoverA(self, columna, fila):
        """ valida si esta ficha puede moverse a otra posici�n
        este M�todo debe ser redefinido."""
        return False

# -*- encoding: utf-8 -*-
from organizadores.ajedrez_basico import AjedrezTradicional
from organizadores.acomodar_fichas import AcomodarFichas

class Reglas(object):

    def __init__(self, personalizado=False):
        self.bandos = ['blanco', 'negro']
        self.turno = 0
        self.partida = None
        self.celda_seleccionada = None
        self.personalizado = personalizado

    def definir_partida(self, partida):
        self.partida = partida

    def pasar_turno(self):
        self.turno = (self.turno+1)%2

    def turno_actual(self):
        return self.bandos[self.turno]

    def obtener_organizador(self):
        """retorna el organizador de fichas en el tablero"""
        if self.personalizado:
            return AcomodarFichas
        else:
            return AjedrezTradicional

    def decir(self, texto, interrumpir=True):
        self.partida.decir(texto, interrumpir)

    def log(self, *args, **kwargs):
        self.partida.pilas.log(*args, **kwargs)

    def seleccionar_celda(self, columna, fila):
        """metodo que se ejecuta al seleccionar una celda.
        este metodo se debe redefinir"""
        pass

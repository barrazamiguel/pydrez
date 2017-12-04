# -*- encoding: utf-8 -*-
from .efecto import EfectoCelda

class FxAgua(EfectoCelda):

    def configurarCelda(self, celda):
        """se aplica al iniciarse en una celda"""
        self.celda = celda
        celda.definirTipo("azul")

    def __str__(self):
        return "agua"
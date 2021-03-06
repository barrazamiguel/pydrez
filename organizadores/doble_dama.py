# -*- encoding: utf-8 -*-
from .organizador_de_fichas import OrganizadorDeFichas

class OrganizadorDobleDama(OrganizadorDeFichas):

    def organizar_fichas(self):
        """acomoda las fichas de un ajedrez tradicional."""
        self.tablero.pilas.log("inicia el organizador... Acomoda el tablero como un ajedrez tradicional")
        self.acomodarPiezas(fila=0, color="blanco")
        self.acomodarPeones(fila=1, color="blanco")
        self.acomodarPiezas(fila=self.tablero.filas-1, color="negro")
        self.acomodarPeones(fila=self.tablero.filas-2, color="negro")
        self.tablero.pilas.log("Finaliza el organizador... termina de acomodar el tablero como un ajedrez tradicional")

    def acomodarPiezas(self, fila, color):
        self.colocar('torre', color, 0, fila)
        self.colocar('caballo', color, 1, fila)
        self.colocar('alfil', color, 2, fila)
        self.colocar('dama', color, 3, fila)
        self.colocar('rey', color, 4, fila)
        self.colocar('dama', color, 5, fila)
        self.colocar('alfil', color, 6, fila)
        self.colocar('caballo', color, 7, fila)
        self.colocar('torre', color, 8, fila)

    def acomodarPeones(self, fila, color):
        for x in range(9):
            self.colocar('peon', color, x, fila)

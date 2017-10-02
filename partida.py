# -*- encoding: utf-8 -*-
from sonido import Sonido
from fichas.pool import PoolDeFichas

class Partida(object):

    def __init__(self, pilas, tts):
        self.pilas = pilas
        self.decir = tts
        self.pool = PoolDeFichas(pilas)
        self.reglas = None
        self.tablero = None
        self.activa = False
        # sonidos de la partida:
        self.sonido_mover = Sonido('audio/mover-ficha.ogg')

    def definir_reglas(self, reglas):
        self.reglas = reglas
        self.reglas.definir_partida(self)

    def definir_tablero(self, tablero):
        self.tablero = tablero
        self.pool.definir_tablero(self.tablero)

    def iniciar(self, *args, **kwargs):
        """Inicia la partida."""
        self.activa = True
        organizador = self.reglas.obtener_organizador()
        self.tablero.acomodarFichas(organizador(pool=self.pool, *args, **kwargs))

    def reiniciar(self):
        """reinicia la partida."""
        # elimina las fichas del tablero.
        # reinicia el historial de movimientos.
        # vuelve a iniciar la partida.
        print("reiniciando")
        pass

    def finalizar(self):
        """finaliza la partida"""
        self.activa = False
        self.decir("jacke mate. fin de la partida.", False)

    def seleccionar_celda(self, columna, fila):
        """Realiza una seleccion de celda si la partida esta activa"""
        if self.activa:
            self.reglas.seleccionar_celda(columna, fila)

    def registrar_movimiento(self, ficha, fichaEliminada, celda_origen, celda_destino):
        self.sonido_mover.reproducir()
        if fichaEliminada:
            print("fuera de juego", fichaEliminada.nombre,  fichaEliminada.color)

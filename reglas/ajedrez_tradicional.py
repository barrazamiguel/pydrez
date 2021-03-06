# -*- encoding: utf-8 -*-
from .reglas import Reglas
from sonido import Sonido

class ReglasAjedrezTradicional(Reglas):

    def __init__(self, *args, **kwargs):
        Reglas.__init__(self, *args, **kwargs)
        self.sonido_revote = Sonido("audio/boing.ogg")
        self.fichaRey = "rey"

    def seleccionar_celda(self, columna, fila):
        """Selecciona una celda.
        solo se puede seleccionar celdas que tienen fichas.
        si ya hay una seleccionada realiza un movimiento
        """

        if self.celda_seleccionada is None:
            # si no hay ninguna celda seleccionada:
            celda = self.partida.tablero.obtener_celda(columna, fila)
            if celda.tiene_ficha():
                turno_actual = self.turno_actual()
                if celda.ficha.color == turno_actual:
                    # seleccionamos la celda:
                    self.celda_seleccionada = celda
                    self.celda_seleccionada.seleccionar()
                    celda.ficha.seleccionar()
                    self.decir(str(self.celda_seleccionada.ficha)+" seleccionado")
                else:
                    self.decir("es turno del "+turno_actual)

        else:
            # si ya hay celda seleccionada:
            if self.celda_seleccionada.columna == columna and  self.celda_seleccionada.fila == fila:
                # si selecciona 2 veces la misma celda la deselecciona.
                self.decir(str(self.celda_seleccionada.ficha)+" deseleccionado")
                self._deseleccionarCelda()
            else:
                # si selecciona otra celda realiza el movimiento:
                self.mover_ficha(columna, fila)

    def mover_ficha(self, columna, fila):
        ficha = self.celda_seleccionada.ficha
        celda = self.partida.tablero.obtener_celda(columna, fila)
        # verificamos si la celda tiene ficha:
        if celda.tiene_ficha():
            # si tiene ficha verificamos que no sea del mismo color:
            celdaVerificada = ficha.color != celda.ficha.color
        else:
            celdaVerificada = True

        if ficha.puede_mover(celda) and celdaVerificada:
            # puede realizar el movimiento:

            self.partida.registrar_movimiento(ficha=self.celda_seleccionada.ficha,
                fichaEliminada=celda.ficha,
                celdaOrigen=self.celda_seleccionada,
                celdaDestino=celda)

            # verificamos si enroca:
            if ficha.nombre == "rey" and (celda_origen.fila in [0,7] and abs(celda_origen.columna - celda_destino.columna) == 2):
                # enroca:
                if celda_destino.columna == 6:
                    #enroque corto:
                    self.acomodarTorreDeEnroque(largo=False)
                else:
                    # enroque largo:
                    self.acomodarTorreDeEnroque(largo=True)


            if celda.ficha is not None:
                celda.ficha.efectoAlEliminar()
            self.celda_seleccionada.liberar()
            # valida si se comio el rey para finalizar la partida:
            if celda.ficha is not None and celda.ficha.nombre == self.fichaRey:
                self.partida.finalizar(motivo="jacke mate", color=self.colorOpuesto(celda.ficha.color))

            self.partida.tablero.posicionar(ficha, columna=columna, fila=fila)
            self.pasar_turno()
            self._deseleccionarCelda()
            self.partida.finalizaMovimiento(celda)
        else:
            # no puede realizar el movimiento:
            self._deseleccionarCelda()
            self.movimiento_imposible()

    def colorOpuesto(self, color):
        if color == "blanco":
            return "negro"
        else:
            return "blanco"

    def _deseleccionarCelda(self):
        """deselecciona una celda seleccionada:
        precondici�n: debe haber una celda seleccionada.
        la propiedad: celda_seleccionada no debe ser None"""
        self.celda_seleccionada.deseleccionar()
        self.celda_seleccionada = None

    def movimiento_imposible(self):
        """metodo que se ejecuta cuando un jugador realiza un movimiento imposible"""
        self.sonido_revote.reproducir()
        self.decir("movimiento imposible")

    def acomodarTorreDeEnroque(self, largo=True):
        print("enroca")
        if not largo:
            #enroque corto:
            c = self.partida.tablero.obtener_celda(7, 0)
            self.partida.tablero.posicionar(c.ficha, columna=5, fila=0)
            c.liberar()
        else:
            # enroque largo:
            c = self.partida.tablero.obtener_celda(0, 0)
            self.partida.tablero.posicionar(c.ficha, columna=3, fila=0)
            c.liberar()

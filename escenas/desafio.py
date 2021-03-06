# -*- encoding: utf-8 -*-
import pilasengine

from actores.tablero import Tablero
from actores.cabezal import Cabezal
from actores.reloj import Reloj
from partida import Partida
from actores.textoAyuda import TextoAyuda
from actores.historial import Historial

from tts import leer as tts
from sonido import Sonido

class Desafio(pilasengine.escenas.Escena):

    def iniciar(self, pilas, nombreDesafio):
        musica = pilas.datos.musica
        if musica is not None:
            musica.detener_gradualmente(3)

        self.fondo = pilas.fondos.FondoMozaico("imagenes/fondo/fondoJuego.jpg")
        self.decir = tts
        self.partida = Partida(pilas)
        self.partida.definir_reglas("puzzle")
        self.textoAyuda = TextoAyuda(self.pilas)

        # se arma el reloj
        self.reloj = Reloj(pilas, x=-150, y=300, incremental=True)

        self.reloj.comenzar()

        # armamos tablero:
        self.tablero = Tablero(pilas, x=- 400 ,y=-250, filas=8, columnas=8)
        self.partida.definir_tablero(self.tablero)

        # definimos la posicion inicial:
        fichas = self.cargarDesafio("datos/desafios/"+ nombreDesafio +".chess")
        self.nombreDesafio = nombreDesafio
        self.partida.iniciar(posicionInicial=fichas)
        self.cabezal = Cabezal(pilas, tablero=self.tablero, tts=tts)

        # conexiones con eventos:
        self.pilas.eventos.pulsa_tecla.conectar(self.interpreta_teclado)
        self.pilas.eventos.click_de_mouse.conectar(self.click_mouse)
        self.pilas.eventos.pulsa_tecla_escape.conectar(self.activar_menu_principal)

        # eventos de partida:
        self.partida.eventoPreMueveFicha.conectar(self.mueveFicha)
        self.partida.eventoFinalizar.conectar(self.finalizar)

        # sonidos:
        self.sonido_mover = Sonido('audio/mover-ficha.ogg')
        self.historial = Historial(pilas, ejex=300, ejey=0, cantidadDeJugadores=1 )
        self.historial.fijo = True

    def activar_menu_principal(self, evento):
        self.pilas.escenas.MenuPrincipal(pilas=self.pilas)


    def mueveFicha(self, evento):
        self.sonido_mover.reproducir()

        if evento.fichaEliminada:
            self.decir(str(evento.ficha) +" por "+ str(evento.fichaEliminada) +" de "+ repr(evento.celdaDestino))
            self.historial.agregar(repr(evento.ficha) + "x" + repr(evento.celdaDestino))
        else:
            self.decir(str(evento.ficha)+" mueve a: "+repr(evento.celdaDestino))
            self.historial.agregar(repr(evento.ficha) + repr(evento.celdaDestino))

    def click_mouse(self, evento):
        x = int(evento.x) - (self.tablero.x - self.tablero.distancia / 2) + self.pilas.camara.x
        y = int(evento.y) - (self.tablero.y - self.tablero.distancia / 2) + self.pilas.camara.y
        columna = x / self.tablero.distancia
        fila = y / self.tablero.distancia
        if(evento.boton == 1):
            self.cabezal.mover(columna=columna, fila=fila)
            self.partida.seleccionar_celda(columna=self.cabezal.columna, fila=self.cabezal.fila)
        if(evento.boton == 2):
            ficha = self.tablero.obtenerFicha(columna=columna,fila=fila)
            if ficha is not None:
                self.textoAyuda.infoDePieza(ficha.nombre,x,y)

    def interpreta_teclado(self, evento):
        if evento.codigo == "a" or evento.codigo == self.pilas.simbolos.IZQUIERDA:
            self.cabezal.mover_izquierda()
        if evento.codigo == "d" or evento.codigo == self.pilas.simbolos.DERECHA:
            self.cabezal.mover_derecha()
        if evento.codigo == "s" or evento.codigo == self.pilas.simbolos.ABAJO:
            self.cabezal.mover_abajo()
        if evento.codigo == "w" or evento.codigo == self.pilas.simbolos.ARRIBA:
            self.cabezal.mover_arriba()
        if evento.codigo == "n":
            self.pilas.escenas.Desafio(pilas=self.pilas, nombreDesafio = self.nombreDesafio)
        if evento.codigo == self.pilas.simbolos.SELECCION:
            self.partida.seleccionar_celda(columna=self.cabezal.columna, fila=self.cabezal.fila)
        if evento.codigo == "F1":
            ficha = self.tablero.obtenerFicha(columna=self.cabezal.columna, fila=self.cabezal.fila)
            if ficha is not None:
                self.textoAyuda.infoDePieza(ficha.nombre,self.cabezal.x + 30,self.cabezal.y)

    def cargarDesafio(self, rutaDeArchivo):
        file = open(rutaDeArchivo, "r")
        info = file.read()
        file.close()

        info = info.split("\n")
        lista = []

        for x in info:
            if x != "":
                x=x.split(" ")
                x.append(int(x[2][1])-1)
                x[2] = ord(x[2][0])-97
                lista.append(tuple(x))

        return lista

    def finalizar(self, evento):
        if evento.motivo == "superado":
            if self.nombreDesafio == '9':
                self.pilas.escenas.GanasteLosDesafios(self.pilas)
            else:
                self.pilas.escenas.DesafioSuperado(self.pilas,self.reloj.texto, self.nombreDesafio)

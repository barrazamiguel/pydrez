# -*- encoding: utf-8 -*-
from pilasengine.actores.actor import Actor

class TextoAyuda(Actor):

    def iniciar(self):
        self.imagen = "invisible.png"



    def infoDePieza(self,nombre, x , y):
        file = open("datos/ayuda/"+nombre+".ayuda", "r")
        info = file.read()
        file.close()

        self.x = 450
        self.y = -250
        self.decir(info)
        return info

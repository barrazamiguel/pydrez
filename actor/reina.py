from pilasengine.actores.actor import Actor

class Reina(Actor):

    def iniciar(self, color="blanco"):
        self.imagen = "imagenes/pieza/"+color+"/reina.png"
        self.bando = color
        self.escala = 0.7



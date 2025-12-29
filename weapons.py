import pygame

class Weapon():
    def __init__(self, image):
        self.image = image
        self.angulo = 0
        self.forma = self.image.get_rect(center = (constante.ANCHO_PERSONAJE, constante.ALTO_PERSONAJE))

    def update(self, personaje):
        self.forma.center = personaje.forma.center
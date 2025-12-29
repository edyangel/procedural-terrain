import pygame
import constantes

class Personaje():
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        self.direccion = "abajo"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animaciones[self.direccion][self.frame_index]

        self.forma = pygame.Rect(0, 0, constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)
        self.forma.center = (x, y)

    def update(self):
        cooldown_animacion = 200
        self.image = self.animaciones[self.direccion][self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animaciones[self.direccion]):
            self.frame_index = 0

        self.image = self.animaciones[self.direccion][self.frame_index]

    def movimiento(self, delta_x, delta_y):
        if delta_x < 0:
            self.direccion = "izquierda"
        elif delta_x > 0:
            self.direccion = "derecha"
        
        if delta_y < 0:
            self.direccion = "arriba"
        elif delta_y > 0:
            self.direccion = "abajo"

        # Si NO se mueve en ninguna dirección, frame 0 (quieto)
        if delta_x == 0 and delta_y == 0:
            self.frame_index = 0

        self.forma.x += delta_x
        self.forma.y += delta_y

    def dibujar(self, interfaz):
        imagen_actual = self.animaciones[self.direccion][self.frame_index]
        interfaz.blit(imagen_actual, self.forma)
        pygame.draw.rect(interfaz, constantes.COLOR_PERSONAJE, self.forma, 1)

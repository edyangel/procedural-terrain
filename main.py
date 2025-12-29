import pygame
import sys
import constantes
from personaje import Personaje
from mapa import Mapa

pygame.init()
ventana = pygame.display.set_mode((constantes.ANCHO_PANTALLA, constantes.ALTO_PANTALLA))
pygame.display.set_caption("farm island")

# --- CARGAR JUGADOR ---
player_image = pygame.image.load("assets/texture/jugador/walk.png")
animaciones = {
    "arriba": [],
    "abajo": [],
    "izquierda": [],
    "derecha": []
}
direcciones = ["arriba", "abajo", "izquierda", "derecha"]

for fila, direccion in enumerate(direcciones):
    for columna in range(4):
        ubicacion_x = columna * constantes.ANCHO_PERSONAJE
        ubicacion_y = fila * constantes.ALTO_PERSONAJE
        rectangulo = pygame.Rect(ubicacion_x, ubicacion_y, constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)
        
        frame = player_image.subsurface(rectangulo)
        frame_escalado = pygame.transform.scale(frame, 
            (frame.get_width() * constantes.SCALE_PERSONAJE, 
            frame.get_height() * constantes.SCALE_PERSONAJE))
        
        animaciones[direccion].append(frame_escalado)

jugador = Personaje(250,250, animaciones)

# --- CARGAR MAPA ---
mapa_juego = Mapa()

# --- VARIABLES JUEGO ---
mover_arriba = False
mover_abajo = False
mover_derecha = False
mover_izquierda = False

reloj = pygame.time.Clock()
run = True

# --- BUCLE PRINCIPAL ---
while run == True:
    reloj.tick(constantes.FPS)
    ventana.fill(constantes.COLOR_BG)

    # 1. DIBUJAR MAPA (Fondo)
    mapa_juego.dibujar(ventana)

    # 2. LOGICA JUGADOR
    delta_x = 0
    delta_y = 0

    if mover_derecha == True: delta_x = 5
    if mover_izquierda == True: delta_x = -5
    if mover_arriba == True: delta_y = -5
    if mover_abajo == True: delta_y = 5

    jugador.movimiento(delta_x, delta_y)
    jugador.update()
    
    # 3. DIBUJAR JUGADOR (Encima del mapa)
    jugador.dibujar(ventana)

    # 4. EVENTOS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            run = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a: mover_izquierda = True
            if evento.key == pygame.K_d: mover_derecha = True
            if evento.key == pygame.K_w: mover_arriba = True
            if evento.key == pygame.K_s: mover_abajo = True

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a: mover_izquierda = False
            if evento.key == pygame.K_d: mover_derecha = False
            if evento.key == pygame.K_w: mover_arriba = False
            if evento.key == pygame.K_s: mover_abajo = False

    pygame.display.update()

pygame.quit()

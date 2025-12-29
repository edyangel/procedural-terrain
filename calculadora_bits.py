import pygame
import sys

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)    # Tierra
AZUL = (0, 0, 255)     # Agua (Vecino Activo)
ROJO = (255, 0, 0)     # Texto

# Configuración
ANCHO_VENTANA = 600
ALTO_VENTANA = 600
TAMANO_CELDA = 150
MARGEN = 10

# Valores de Bits (Bitmask)
VALORES = [
    [16, 1, 32],   # Arr-Izq, Arriba, Arr-Der
    [2,  0, 4],    # Izq,     YO,     Der
    [64, 8, 128]   # Abj-Izq, Abajo, Abj-Der
]

# Estado de los vecinos (True = Agua/Activo, False = Tierra/Inactivo)
# Matriz 3x3
estado = [
    [False, False, False],
    [False, False, False],
    [False, False, False]
]

def main():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Calculadora de Bits - Haz Clic en los Vecinos")
    fuente = pygame.font.SysFont("Arial", 40)
    fuente_gigante = pygame.font.SysFont("Arial", 100)

    while True:
        # 1. Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                # Calcular en qué celda se hizo clic
                # Ajustamos para centrar la cuadrícula de 3x3
                inicio_x = 50
                inicio_y = 50
                
                col = (mx - inicio_x) // (TAMANO_CELDA + MARGEN)
                fila = (my - inicio_y) // (TAMANO_CELDA + MARGEN)

                if 0 <= fila < 3 and 0 <= col < 3:
                    if fila == 1 and col == 1:
                        pass # No hacemos nada al clic en el centro (YO)
                    else:
                        estado[fila][col] = not estado[fila][col] # Invertir estado

        # 2. Dibujar
        ventana.fill(NEGRO)
        
        suma_total = 0
        inicio_x = 50
        inicio_y = 50

        for f in range(3):
            for c in range(3):
                x = inicio_x + c * (TAMANO_CELDA + MARGEN)
                y = inicio_y + f * (TAMANO_CELDA + MARGEN)
                
                color = VERDE # Por defecto Tierra
                valor = VALORES[f][c]

                # Si es el centro (YO)
                if f == 1 and c == 1:
                    color = (100, 100, 100) # Gris
                # Si es vecino y está activo
                elif estado[f][c]:
                    color = AZUL
                    suma_total += valor
                
                pygame.draw.rect(ventana, color, (x, y, TAMANO_CELDA, TAMANO_CELDA))
                
                # Dibujar el valor del bit en pequeño
                if not (f==1 and c==1):
                    texto_bit = fuente.render(str(valor), True, NEGRO)
                    ventana.blit(texto_bit, (x + 10, y + 10))

        # 3. Dibujar la Suma Total en el Centro
        texto_suma = fuente_gigante.render(str(suma_total), True, BLANCO)
        rect_suma = texto_suma.get_rect(center=(ANCHO_VENTANA//2, ALTO_VENTANA - 80))
        ventana.blit(texto_suma, rect_suma)
        
        instruccion = fuente.render("Suma Total (Mask):", True, BLANCO)
        ventana.blit(instruccion, (ANCHO_VENTANA//2 - 150, ALTO_VENTANA - 130))

        pygame.display.flip()

if __name__ == "__main__":
    main()

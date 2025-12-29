import pygame
import constantes
import random

class Mapa:
    def __init__(self):
        # 1. Cargar la imagen del tileset
        self.terreno_img = pygame.image.load("assets/texture/terreno/Hills.png")
        self.terreno_img_arena = pygame.image.load("assets/texture/terreno/Arena.png")
        self.lista_tiles = []
        self.mapa_nivel = []
        
        # 2. Cortar los tiles
        self.cortar_tiles()
        
        # 3. Generar el nivel
        self.generar_nivel()

    def cortar_tiles(self):
        for fila in range(9):  # 0 1 2 3 4 5 6 7 8
            for columna in range(11):
                x = columna * constantes.TILE_SIZE
                y = fila * constantes.TILE_SIZE
                rect = pygame.Rect(x, y, constantes.TILE_SIZE, constantes.TILE_SIZE)
                tile = self.terreno_img.subsurface(rect)
                # Si quieres escalar:
                # tile = pygame.transform.scale(tile, (constantes.TILE_SIZE * constantes.TILE_SCALE, ...))
                self.lista_tiles.append(tile)

        for fila in range(7):
            for columna in range(11):
                x = columna * constantes.TILE_SIZE
                y = fila * constantes.TILE_SIZE
                rect = pygame.Rect(x, y, constantes.TILE_SIZE, constantes.TILE_SIZE)
                tile = self.terreno_img_arena.subsurface(rect)
                self.lista_tiles.append(tile)

    def suavizar(self):
        # Creamos un mapa nuevo temporal para no leer y escribir al mismo tiempo
        nuevo_mapa = []
        
        for f in range(constantes.FILAS_MAPA):
            nueva_fila = []
            for c in range(constantes.COLUMNAS_MAPA):
                
                vecinos_tierra = 0
                vecinos_arena = 0
                
                # Revisamos un area de 3x3 alrededor de la celda
                for y in range(f - 1, f + 2):
                    for x in range(c - 1, c + 2):
                        # Asegurarnos de no salirnos del mapa
                        if x >= 0 and y >= 0 and x < constantes.COLUMNAS_MAPA and y < constantes.FILAS_MAPA:
                            val = self.mapa_nivel[y][x]
                            if val == constantes.TIERRA:
                                vecinos_tierra += 1
                            elif val == constantes.ARENA:
                                vecinos_arena += 1
                
                # Reglas de Biomas:
                if vecinos_tierra > 4:
                    nueva_fila.append(constantes.TIERRA)
                elif vecinos_arena > 4:
                    nueva_fila.append(constantes.ARENA)
                else:
                    nueva_fila.append(constantes.AGUA)
            
            nuevo_mapa.append(nueva_fila)
            
        # Actualizamos el mapa real
        self.mapa_nivel = nuevo_mapa

    def generar_nivel(self):
        for f in range(constantes.FILAS_MAPA):
            fila_nueva = []
            for c in range(constantes.COLUMNAS_MAPA):

                suerte = random.randint(0,100)

                if suerte < 5:
                    fila_nueva.append(constantes.AGUA)
                elif suerte < 55:
                    fila_nueva.append(constantes.ARENA)
                else:
                    fila_nueva.append(constantes.TIERRA)

            self.mapa_nivel.append(fila_nueva)
        
        # 2. Suavizar (Crear islas)
        for i in range(3):
             self.suavizar()

        # 3. Aplicar Bordes
        self.aplicar_autotiling()

    def es_inferior(self,tile_yo, tile_vecino):
        #El vecino es de un material mas alto que yo?
        
        if tile_yo == constantes.TIERRA:
            return (tile_vecino == constantes.AGUA or tile_vecino == constantes.ARENA)

        if tile_yo == constantes.ARENA:
            return (tile_vecino == constantes.AGUA)
        print(f"Yo: {tile_yo}, Vecino: {tile_vecino}, Es inf? {condicion}")
        return False # si soy agua, nadie es inferior a mi

    def calcular_mask(self, f, c, yo):
        mask = 0
        # Cardinales (1, 2, 4, 8)
        if self.es_inferior(yo, self.mapa_nivel[f-1][c]): mask += 1
        if self.es_inferior(yo, self.mapa_nivel[f][c-1]): mask += 2
        if self.es_inferior(yo, self.mapa_nivel[f][c+1]): mask += 4
        if self.es_inferior(yo, self.mapa_nivel[f+1][c]): mask += 8
        
        # Diagonales (16, 32, 64, 128) - Ahora SIEMPRE se suman
        if self.es_inferior(yo, self.mapa_nivel[f-1][c-1]): mask += 16
        if self.es_inferior(yo, self.mapa_nivel[f-1][c+1]): mask += 32
        if self.es_inferior(yo, self.mapa_nivel[f+1][c-1]): mask += 64
        if self.es_inferior(yo, self.mapa_nivel[f+1][c+1]): mask += 128
        
        return mask

    def aplicar_autotiling(self):
        for f in range(1, constantes.FILAS_MAPA - 1):
            for c in range(1, constantes.COLUMNAS_MAPA - 1):
                yo = self.mapa_nivel[f][c]

                offset = 0
                if yo == constantes.TIERRA: offset = 0
                elif yo == constantes.ARENA: offset = constantes.OFFSET_ARENA
                else: continue

                # 1. Calculo Unificado (Full Bitmask)
                mask = self.calcular_mask(f, c, yo)
                
                # DEBUG: Ver que numeros raros salen
                if f == 10 and c == 10:
                    print(f"DEBUG(10,10): Yo={yo} Mask={mask}")

                # 2. Buscar en el Diccionario (Con Plan B)
                # Intento A: Busqueda Exacta
                nuevo_tile = constantes.REGLAS_TILES.get(mask)
                
                # Intento B: Si no existe, usamos la version simplificada (Sin diagonales)
                if nuevo_tile is None:
                    mask_simple = mask & 15
                    nuevo_tile = constantes.REGLAS_TILES.get(mask_simple, yo)
                
                if nuevo_tile != yo:
                     self.mapa_nivel[f][c] = nuevo_tile + offset

    def dibujar(self, superficie):
        for f in range(len(self.mapa_nivel)):
            for c in range(len(self.mapa_nivel[f])):
                tile_id = self.mapa_nivel[f][c]
                imagen = self.lista_tiles[tile_id]
                
                # Calcular posición en pantalla
                x = c * constantes.TILE_SIZE
                y = f * constantes.TILE_SIZE
                
                # CORRECCION FONDO NEGRO:
                # Si el tile actual NO es agua, dibujamos agua debajo primero
                if tile_id != constantes.AGUA:
                    superficie.blit(self.lista_tiles[constantes.AGUA], (x, y))

                superficie.blit(imagen, (x, y))

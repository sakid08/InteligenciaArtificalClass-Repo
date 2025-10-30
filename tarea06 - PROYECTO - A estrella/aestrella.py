import pygame
import math

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Algoritmo A*")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (251, 43, 223)
VERDE = (0, 255, 0)
GRIS2 = (226, 226, 226)
AMARILLO = (255, 250, 84)

# X, Y
orden_revision = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]


class Nodo:
    def __init__(self, fila, col, ancho, total_filas, n_nodo, n_padre, g_costo=float('inf'), h_heuristica=float('inf')):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.n_nodo = n_nodo
        self.n_padre = n_padre
        self.g_costo = g_costo
        self.h_heuristica = h_heuristica
    
    def get_datos_nodo(self):
        f_total = self.g_costo + self.h_heuristica
        return self.n_nodo, self.n_padre, self.g_costo, self.h_heuristica, f_total
    
    def set_n_nodo(self, n_nodo):
        self.n_nodo = n_nodo

    def set_n_padre(self, n_padre):
        self.n_padre = n_padre

    def set_g_costo(self, g_costo):
        self.g_costo = g_costo

    def set_h_heuristica(self, h_heuristica):
        self.h_heuristica = h_heuristica

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))


def h(p1_pos, p2_pos):
    fila1, col1 = p1_pos
    fila2, col2 = p2_pos
    dx = abs(fila1 - fila2)
    dy = abs(col1 - col2)
    
    # Costo diagonal (sqrt(2)) y costo ortogonal (1)
    costo_diagonal = math.sqrt(2)
    costo_ortogonal = 1

    return (costo_ortogonal * (max(dx, dy) - min(dx, dy)) + costo_diagonal * min(dx, dy))


def reconstruir_camino(ventana, grid, filas, ancho, nodo_actual):
    while nodo_actual.n_padre is not None:
        nodo_actual = nodo_actual.n_padre
        if not nodo_actual.es_inicio():
            nodo_actual.color = VERDE

def iniciar_algoritmo(ventana, grid, filas, ancho, inicio, fin, lista_abierta, lista_cerrada):
    lista_abierta.clear()
    lista_cerrada.clear()
    
    inicio.set_g_costo(0)
    h_score_inicio = h(inicio.get_pos(), fin.get_pos())
    inicio.set_h_heuristica(h_score_inicio)
    
    contador_nodos = 1
    inicio.set_n_nodo(contador_nodos)
    
    if not no_repetidos(lista_abierta, inicio):
        lista_abierta.append(inicio)
    
    while len(lista_abierta) > 0:
        # Encontrar el nodo en lista_abierta con el menor f_score
        nodo_actual = lista_abierta[0]
        idx_actual = 0
        for i, nodo in enumerate(lista_abierta):
            _, _, g_nodo, _, f_nodo = nodo.get_datos_nodo()
            _, _, g_actual, _, f_actual = nodo_actual.get_datos_nodo()

            # toma el menor f; si empatan
            if f_nodo < f_actual or (f_nodo == f_actual and g_nodo > g_actual):
                nodo_actual = nodo
                idx_actual = i

                
        lista_abierta.pop(idx_actual)
        if not no_repetidos(lista_cerrada, nodo_actual):
            lista_cerrada.append(nodo_actual)
        
        if not nodo_actual.es_inicio():
            nodo_actual.color = AMARILLO
        
        if nodo_actual == fin:
            reconstruir_camino(ventana, grid, filas, ancho, fin)
            fin.hacer_fin()
            inicio.hacer_inicio()
            return True 

        vecinos = se_pueden_usar(grid, nodo_actual)
        
        for vecino in vecinos:
            if no_repetidos(lista_cerrada, vecino):
                continue
                
            costo = 1.0
            if abs(vecino.fila - nodo_actual.fila) == 1 and abs(vecino.col - nodo_actual.col) == 1:
                costo = math.sqrt(2)
            
            g_tentativo = nodo_actual.g_costo + costo
            
            if g_tentativo < vecino.g_costo:
                vecino.set_n_padre(nodo_actual)
                vecino.set_g_costo(g_tentativo)
                
                h_score_vecino = h(vecino.get_pos(), fin.get_pos()) * 1.0001
                vecino.set_h_heuristica(h_score_vecino)

                if not no_repetidos(lista_abierta, vecino):
                    contador_nodos += 1
                    vecino.set_n_nodo(contador_nodos)
                    lista_abierta.append(vecino)
                    vecino.color = GRIS2

        
        dibujar(ventana, grid, filas, ancho)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

    return False


def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas, None, None)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def no_repetidos(lista, nuevo_dato):
    longitud = len(lista)
    for i in range(longitud):
        if lista[i] == nuevo_dato:
            return True
    return False

def negUno_a_uno(max_limite, num):
    min_limite = 0
    if num >= min_limite and num < max_limite:
        return True
    return False

def se_pueden_usar(grid, nodo_actual):
    fila_actual = nodo_actual.fila
    col_actual = nodo_actual.col
    max_filas = len(grid)
    lista_usables = []

    for offset in orden_revision: 
        offset_fila = offset[0]
        offset_col = offset[1]
        
        nueva_fila = fila_actual + offset_fila
        nueva_col = col_actual + offset_col
        
        if negUno_a_uno(max_filas, nueva_fila) and negUno_a_uno(max_filas, nueva_col):
            vecino = grid[nueva_fila][nueva_col]
            
            if not vecino.es_pared():
                
                es_diagonal = (offset_fila != 0 and offset_col != 0)
                
                if es_diagonal: 
                    # Comprobar flancos
                    fila_flanco_1 = fila_actual
                    col_flanco_1 = col_actual + offset_col
                    
                    fila_flanco_2 = fila_actual + offset_fila
                    col_flanco_2 = col_actual

                    pared_en_flanco_1 = grid[fila_flanco_1][col_flanco_1].es_pared()
                    pared_en_flanco_2 = grid[fila_flanco_2][col_flanco_2].es_pared()
                    
                    
                    if not pared_en_flanco_1 or not pared_en_flanco_2:
                        lista_usables.append(vecino)
                
                else:
                    # Si no es diagonal, siempre es válido (si no es pared)
                    lista_usables.append(vecino)
                            
    return lista_usables


def main(ventana, ancho):
    FILAS = 11
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    lista_abierta = []
    lista_cerrada = []

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                
                if 0 <= fila < FILAS and 0 <= col < FILAS:
                    nodo = grid[fila][col]
                    if not inicio and nodo != fin:
                        inicio = nodo
                        inicio.hacer_inicio()

                    elif not fin and nodo != inicio:
                        fin = nodo
                        fin.hacer_fin()

                    elif nodo != fin and nodo != inicio:
                        nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                
                if 0 <= fila < FILAS and 0 <= col < FILAS:
                    nodo = grid[fila][col]
                    nodo.restablecer()
                    if nodo == inicio:
                        inicio = None
                    elif nodo == fin:
                        fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            if nodo.color == GRIS2 or nodo.color == AMARILLO or nodo.color == VERDE:
                                nodo.restablecer()

                            nodo.set_n_nodo(None)
                            nodo.set_n_padre(None)
                            nodo.set_g_costo(float('inf'))
                            nodo.set_h_heuristica(float('inf'))
                    
                    encontrado = iniciar_algoritmo(ventana, grid, FILAS, ancho, inicio, fin, lista_abierta, lista_cerrada)
                    
                    if not encontrado:
                        print("¡ALGORITMO TERMINADO! No se encontró un camino.")

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
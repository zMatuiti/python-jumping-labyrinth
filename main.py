import pygame
import sys
import heapq

TAM_CELDA = 60
MARGEN = 5
COLOR_FONDO = (255, 255, 255)
COLOR_CELDA = (200, 200, 200)
COLOR_INICIO = (100, 255, 100)  # verde
COLOR_META = (255, 100, 100)  # rojo
COLOR_TEXTO = (0, 0, 0)


class Laberinto:
    def __init__(self, m, n, inicio, meta, matriz):
        self.m = m
        self.n = n
        self.inicio = inicio
        self.meta = meta
        self.matriz = matriz

    def leer_archivo(nombre_archivo):
        laberintos = []
        with open(nombre_archivo, 'r') as archivo:
            while True:
                linea = archivo.readline()
                if not linea or linea.strip() == '0':
                    break

                datos = linea.strip().split()
                if len(datos) != 6:
                    continue

                m, n, fi, ci, fm, cm = map(int, datos)
                matriz = []
                for _ in range(m):
                    fila = list(map(int, archivo.readline().strip().split()))
                    matriz.append(fila)
                else:
                    laberintos.append(
                        Laberinto(m, n, (fi, ci), (fm, cm), matriz))
                continue

        return laberintos

    def movimientos_validos(self, pos):
        i, j = pos
        if not (0 <= i < self.m and 0 <= j < self.n):
            return []

        try:
            saltos = self.matriz[i][j]
        except IndexError:
            return []

        movimientos = []
        for di, dj in [(-saltos, 0), (saltos, 0), (0, -saltos), (0, saltos)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.m and 0 <= nj < self.n:
                movimientos.append((ni, nj))
        return movimientos

    def final(self, pos):
        return pos == self.meta


def dfs(laberinto):
    arr = [(laberinto.inicio, [laberinto.inicio])]
    visitados = set()

    while arr:
        actual, path = arr.pop()

        if laberinto.final(actual):
            return len(path) - 1

        if actual in visitados:
            continue

        visitados.add(actual)

        for vecino in laberinto.movimientos_validos(actual):
            if vecino not in visitados:
                arr.append((vecino, path + [vecino]))

    return None


def costo_uniforme(laberinto):
    heap = [(0, laberinto.inicio)]
    visitados = {}

    while heap:
        costo, actual = heapq.heappop(heap)

        if laberinto.final(actual):
            return costo

        if actual in visitados and visitados[actual] <= costo:
            continue

        visitados[actual] = costo

        for vecino in laberinto.movimientos_validos(actual):
            heapq.heappush(heap, (costo+1, vecino))

    return None


def mostrar_laberinto(laberinto):
    try:
        pygame.init()
        ancho = laberinto.n * (TAM_CELDA + MARGEN) + MARGEN
        alto = laberinto.m * (TAM_CELDA + MARGEN) + MARGEN

        pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Laberinto Saltarín")
        fuente = pygame.font.SysFont(None, 24)

        run = True  # flag
        while run:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    run = False

            pantalla.fill(COLOR_FONDO)

            for i in range(laberinto.m):
                for j in range(laberinto.n):
                    try:
                        color = COLOR_CELDA
                        if (i, j) == laberinto.inicio:
                            color = COLOR_INICIO
                        elif (i, j) == laberinto.meta:
                            color = COLOR_META

                        rect = pygame.Rect(
                            j * (TAM_CELDA + MARGEN) + MARGEN,
                            i * (TAM_CELDA + MARGEN) + MARGEN,
                            TAM_CELDA, TAM_CELDA
                        )
                        pygame.draw.rect(pantalla, color, rect)

                        # mostrar G en la meta
                        valor = 'G' if (i, j) == laberinto.meta else str(
                            laberinto.matriz[i][j])
                        texto = fuente.render(valor, True, COLOR_TEXTO)
                        pantalla.blit(texto, (rect.x + 20, rect.y + 20))
                    except IndexError:
                        continue

            pygame.display.flip()

    except Exception as e:
        print(f"Error al mostrar: {e}")
    finally:
        pygame.quit()


def main():
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
    else:
        archivo = "test.txt"

    try:
        laberintos = Laberinto.leer_archivo(archivo)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}")
        return

    resultados_finales = []

    for idx, lab in enumerate(laberintos):
        print(f"\nLaberinto #{idx + 1}")

        pasos_dfs = dfs(lab)
        print(
            f"DFS: {pasos_dfs if pasos_dfs is not None else 'No hay solución'}")

        pasos_ucs = costo_uniforme(lab)
        print(
            f"Costo Uniforme: {pasos_ucs if pasos_ucs is not None else 'No hay solución'}")

        resultados_finales.append(
            str(pasos_ucs) if pasos_ucs is not None else "No hay solución")

        try:
            mostrar_laberinto(lab)
        except Exception as e:
            print(f"Error mostrando laberinto: {e}")

    print("\nResultados finales:")
    for resultado in resultados_finales:
        print(resultado)


if __name__ == "__main__":
    main()

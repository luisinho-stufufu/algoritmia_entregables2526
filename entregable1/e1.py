import sys
from typing import TextIO

from algoritmia.datastructures.queues import Fifo

# --- Comprobamos las versiones de Python y algoritmia ---

def _check_environment(min_py: tuple[int, ...], min_alg: tuple[int, ...]):
    # Comprueba la versión de Python
    if sys.version_info < min_py:
        print(f"Error: Se requiere Python {'.'.join(map(str, min_py))} o superior (detectado {sys.version.split()[0]})")
        sys.exit(1)
    # Comprueba la versión de algoritmia
    try:
        from algoritmia import TVERSION
    except ModuleNotFoundError:
        print("La biblioteca algoritmia no está instalada.")
        sys.exit(1)
    except ImportError:
        TVERSION = (0, 0, 0)
    if TVERSION < min_alg:
        print(f"Error: Se requiere algoritmia >= {'.'.join(map(str, min_alg))}")
        sys.exit(1)

_check_environment((3, 12), (3, 1, 4))  # Versiones mínimas: python 3.12 y algoritmia 3.1.4

# ---- Importamos de la biblioteca algoritmia ---

from algoritmia.datastructures.graphs import UndirectedGraph

# --- Tipos ----

type Vertex = tuple[int, int]
type Edge = tuple[Vertex, Vertex]
type Path = list[Vertex]

# Tipo para las instancias (ver apartado 2.2 del enunciado)
type Data = tuple[int, int, int, int, UndirectedGraph[Vertex]]

# Tipo para los resultados (ver apartado 2.2 del enunciado)
type Result = tuple[Vertex, int, Path, Path]

# --- Funciones auxiliares ---

# Convierte un camino (lista de vértices) en un string con el formato indicado en
# el apartado 2.2 del enunciado.
def _path2str(path: list[Vertex]) -> str:
    return ' # '.join(f'{t[0]} {t[1]}' for t in path)

# --- Funciones ---

# - Recibe un descriptor de fichero de texto que contiene una instancia del problema
#   en el formato descrito en el apartado 1.2 del enunciado.
# - Devuelve la instancia como un objeto de tipo Data.
def read_data(f: TextIO) -> Data:
    calX,calY = tuple(int(s) for s in f.readline().split())
    n_rows,n_cols = tuple(int(s) for s in f.readline().split())
    edges: list[Edge] = []
    for line in f:
        r1,c1,r2,c2 = tuple(int(s) for s in line.split())
        edges.append(((r1,c1),(r2,c2)))
    lab = UndirectedGraph(E = edges)

    return calX,calY,n_rows,n_cols,lab


# Función auxiliar
def bf_search(g: UndirectedGraph[Vertex], source: Vertex) -> tuple[dict[Vertex, int], dict[Vertex, Vertex]]:
    queue: Fifo[Vertex] = Fifo()
    dist: dict[Vertex, int] = {source: 0}
    parent: dict[Vertex, Vertex] = {source: source}

    queue.push(source)
    while len(queue) > 0:
        u = queue.pop()
        for v in g.succs(u):
            if v not in dist:  # no visitado
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.push(v)
    return dist, parent

# - Recibe un objeto de tipo Data con la instancia del problema.
# - Devuelve el resultado como un objeto de tipo Result.
def process(data: Data) -> Result:
    calX, calY, n_rows, n_cols, lab = data
    source: Vertex = (0, 0)
    target: Vertex = (n_rows - 1, n_cols - 1)

    # Ejecutamos BFS desde ambos extremos
    dist_start, parent_start = bf_search(lab, source)
    dist_end, parent_end = bf_search(lab, target)

    # Buscamos el tesoro óptimo
    max_cal: int = -1
    mejor_tesoro: Vertex = source
    for v in lab.V:
        total_cal = calX * dist_start[v] + calY * dist_end[v]
        if total_cal > max_cal:
            max_cal = total_cal
            mejor_tesoro = v

    # Recuperamos los caminos con los parent obtenidos
    def recover_path(parent: dict[Vertex, Vertex], target: Vertex) -> Path:
        path: Path = [target]
        while path[-1] != parent[path[-1]]:
            path.append(parent[path[-1]])
        path.reverse()
        return path

    path1: Path = recover_path(parent_start, mejor_tesoro)
    path2: Path = recover_path(parent_end, mejor_tesoro)
    path2.reverse()

    return mejor_tesoro, max_cal, path1, path2

# - Recibe un objeto de tipo Result con el resultado del problema.
# - Muestra la salida en el formato que se indica en el apartado 1.3 del enunciado
def show_results(result: Result):
    (row, col), total_cal, path1, path2 = result
    print(row, col)
    print(total_cal)
    print(_path2str(path1))
    print(_path2str(path2))

# --- Programa principal ---

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_results(result0)

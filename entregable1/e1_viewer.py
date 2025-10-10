#!/usr/bin/env python3
import sys

# --- Comprobamos las versiones de Python y algoritmia, y que Tkinter esté instalado ---

def _check_environment(min_py: tuple[int, ...], min_alg: tuple[int, ...]):
    # Comprueba la versión de Python
    if sys.version_info < min_py:
        print(f"ERROR: Se requiere Python {'.'.join(map(str, min_py))} o superior (detectado {sys.version.split()[0]})")
        sys.exit(1)
    # Comprueba que tkinter está instalado
    try:
        import tkinter
    except ModuleNotFoundError:
        print("ERROR: Es necesario instalar el paquete Tkinter (En Ubuntu: sudo apt install python3-tk")
        sys.exit(1)
    # Comprueba la versión de algoritmia
    try:
        from algoritmia import TVERSION
    except ModuleNotFoundError:
        print("ERROR: La biblioteca algoritmia no está instalada.")
        sys.exit(1)
    except ImportError:
        TVERSION = (0, 0, 0)
    if TVERSION < min_alg:
        print(f"ERROR: Se requiere algoritmia >= {'.'.join(map(str, min_alg))}")
        sys.exit(1)

_check_environment((3, 12), (3,1,4))  # Versiones mínimas: python 3.12 y algoritmia 3.1.4

# ---- Importaciones de la biblioteca algoritmia ---
from algoritmia.viewers.labyrinth_viewer import LabyrinthViewer

# --- Importamos el modulo del estudiante ---
from e1 import *

# --- Funciones auxiliares -----------------------------------------

def parse_path(line: str) -> list[tuple[int, int]]:
    def tuple2(pair_txt):
        r, c = pair_txt.split()
        return int(r), int(c)
    return [tuple2(pair_txt) for pair_txt in line.split('#')]

# --- Programa principal -----------------------------------------

# El programa tiene dos modos de funcionamiento según el número de parámetros,
# que puede ser 2 o 3.

if len(sys.argv) not in [2, 3]:
    print('Two usage options:')
    print(f'    python3 {sys.argv[0]} <instance_filename> <solution_filename>')
    print(f'    python3 {sys.argv[0]} <instance_filename>')
    sys.exit(1)

# Lee la instancia utilizando tu función 'read_data', si tu función tiene algún bug
# el programa podría no funcionar correctamwente.
with open(sys.argv[1]) as f:
    try:
        data = read_data(f)
    except Exception as e:
        print("Exception running 'read_data':", e)
        sys.exit(1)

try:
    x, y, rows, cols, lab = data
except Exception as e:
    print("Exception unpacking 'data' object:", e)
    sys.exit(1)

entrance_pos = (0, 0)
exit_pos = (rows - 1, cols - 1)

if len(sys.argv) == 3:
    # Lee la solución del fichero de solución
    with open(sys.argv[2]) as f:
        try:
            treasure_pos = tuple(map(int, f.readline().split()))
            total_cal = int(f.readline())
            p1 = parse_path(f.readline())
            p2 = parse_path(f.readline())
        except Exception as e:
            print("Exception reading file '{sys.argv[2]}':", e)
            sys.exit(1)
else:
    # Calcula la solución con tu función 'process'
    try:
        result = process(data)
    except Exception as e:
        print("Exception running 'process':", e)
        sys.exit(1)

    try:
        treasure_pos, total_cal, p1, p2 = result
    except Exception as e:
        print("Exception unpacking 'result':", e)
        sys.exit(1)

lv = LabyrinthViewer(lab, canvas_width=1024, canvas_height=820, margin=4, wall_width=1)

steps1, steps2 = len(p1)-1, len(p2)-1
cal1, cal2 = steps1 * x, steps2 * y
total = cal1 + cal2
lv.title= f"E1 viewer   -   Total calories:  {steps1}·X + {steps2}·Y = {steps1}·{x} + {steps2}·{y} = {cal1} + {cal2} = {total}"

lv.set_input_point(entrance_pos)
lv.set_output_point(exit_pos)
lv.add_marked_cell(treasure_pos, 'yellow')
lv.add_path(p1, 'red', 1)
lv.add_path(p2, 'blue', -1)

lv.run()  # Muestra la ventana gráfica

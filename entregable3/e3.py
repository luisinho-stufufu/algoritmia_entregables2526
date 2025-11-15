import sys
from typing import TextIO

# --- BEGIN Comprobamos las versiones de Python y algoritmia ---

def _check_environment(min_py: tuple[int, ...], min_alg: tuple[int, ...]):
    # Comprueba la versión de Python
    if sys.version_info < min_py:
        print(f"ERROR: Se requiere Python {'.'.join(map(str, min_py))} o superior (detectado {sys.version.split()[0]})")
        sys.exit(1)
    # Comprueba la versión de algoritmia
    try:
        from algoritmia import TVERSION
    except ModuleNotFoundError:
        print("ERROR: La biblioteca algoritmia no está instalada.", file=sys.stderr)
        sys.exit(1)
    except ImportError:
        TVERSION = (0, 0, 0)
    if TVERSION < min_alg:
        print(f"ERROR: Se requiere algoritmia >= {'.'.join(map(str, min_alg))}", file=sys.stderr)
        print("Puedes instalarla/actualizarla desde el terminal de PyCharm con este comando:", file=sys.stderr)
        print("    pip install algoritmia --upgrade", file=sys.stderr)
        sys.exit(1)

_check_environment((3, 12), (4, 0, 6))  # Versiones mínimas: python 3.12 y algoritmia 4.0.6

# --- END Comprobamos las versiones de Python y algoritmia ---

type Data = tuple[int, ...]
type Result = tuple[int, tuple[int, ...]]

def read_data(f: TextIO) -> Data:
    val_esm = tuple(int(linea) for linea in f)
    return val_esm

def process(data: Data) -> Result:
    pass

def show_results(result: Result):
    miner_profit, distribution = result
    print(miner_profit)
    for m in [0, 1, 2, -1]:
        print(' '.join(str(i) for i, d in enumerate(distribution) if d == m))

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_results(result0)

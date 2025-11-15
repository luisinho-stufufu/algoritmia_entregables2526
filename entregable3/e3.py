import sys
from dataclasses import dataclass
from typing import TextIO, Iterator, Self

from algoritmia.schemes.bt_scheme import DecisionSequence, State, bt_solutions, max_solution


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
type Decision = int                         #Minero al que se le asigna la esmeralda

def read_data(f: TextIO) -> Data:
    val_esm = tuple(int(linea) for linea in f)
    return val_esm

def process(data: Data) -> Result:
    val_esm = data
    total = sum(val_esm) // 3

    #Clase extra que almacena las sumas de los mineros en una tupla
    @dataclass
    class Extra:
        sums_min: tuple[int, int, int]

    class EsmeraldasDS (DecisionSequence[Decision,Extra]):

        def is_solution(self) -> bool:
            if len(self) == len(val_esm):
                sums = self.extra.sums_min
                return sums[0] == sums[1] == sums[2]
            return False


        def successors(self) -> Iterator[Self]:
            k = len(self)

            if k < len(val_esm):
                v = val_esm[k]
                s0, s1, s2 = self.extra.sums_min

                if s0 + v <= total:
                    yield self.add_decision(0, Extra((s0 + v, s1, s2)))

                if s1 + v <= total:
                    yield self.add_decision(1, Extra((s0, s1 + v, s2)))

                if s2 + v <= total:
                    yield self.add_decision(2, Extra((s0, s1, s2 + v)))

                yield self.add_decision(-1, self.extra)



        def state(self) -> State:
            return len(self), self.extra.sums_min

    def f(solution_ds: DecisionSequence[Decision, Extra]) -> int:
        return solution_ds.extra.sums_min[0]

    initial_ds = EsmeraldasDS(Extra((0,0,0)))
    all_sols = bt_solutions(initial_ds)
    best_sol = max_solution(all_sols, f)

    if best_sol is None:
        pass

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

import sys
from typing import TextIO, Iterator
from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions, max_solution
from dataclasses import dataclass


# --- BEGIN Comprobamos las versiones de Python y algoritmia ---
def _check_environment(min_py: tuple[int, ...], min_alg: tuple[int, ...]):
    if sys.version_info < min_py:
        print(f"ERROR: Se requiere Python {'.'.join(map(str, min_py))} o superior (detectado {sys.version.split()[0]})")
        sys.exit(1)
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


_check_environment((3, 12), (4, 0, 6))

# --- END Comprobamos las versiones de Python y algoritmia ---

type Data = tuple[int, ...]
# Decisión (D): 0, 1, 2 (minero asignado) o -1 (no repartida).
type Decision = int
# El resultado es (valor_común_minero, tupla_reparto).
type Result = tuple[int, tuple[Decision, ...]]


def read_data(f: TextIO) -> Data:
    val_esm = tuple(int(linea) for linea in f)
    return val_esm


def process(data: Data) -> Result:
    V = data
    N = len(V)

    # La clase Extra almacena el estado de las sumas de los tres mineros.
    @dataclass
    class Extra:
        current_sums: tuple[int, int, int]  # (suma_m0, suma_m1, suma_m2)

    # DecisionSequence para el problema de reparto.
    class FairDistributionDS(DecisionSequence[Decision, Extra]):

        def is_solution(self) -> bool:
            """
            Es solución si: 1. Secuencia completa. 2. Las tres sumas son iguales.
            """
            if len(self) == N:
                sums = self.extra.current_sums
                return sums[0] == sums[1] and sums[1] == sums[2]
            return False

        def successors(self) -> Iterator['FairDistributionDS']:
            """
            Genera los sucesores para la siguiente esmeralda (índice n).
            """
            n = len(self)  # Índice de la esmeralda a asignar
            if n < N:
                v_n = V[n]

                # 1. Asignar a uno de los 3 mineros (m = 0, 1, 2)
                current_sums = list(self.extra.current_sums)
                for m in range(3):
                    new_sums = current_sums[:]
                    new_sums[m] += v_n
                    # No es necesario podar, ya que el objetivo es maximizar S,
                    # y el valor S solo se garantiza al final (en is_solution).
                    yield self.add_decision(m, Extra(tuple(new_sums)))

                # 2. Asignar como no repartida (-1)
                yield self.add_decision(-1, self.extra)

        # Esta función no es estrictamente necesaria si se usa bt_solutions,
        # pero se incluye para seguir la estructura del ejemplo SubsetSumDS.
        def state(self) -> tuple[int, tuple[int, int, int]]:
            return len(self), self.extra.current_sums

    # Función objetivo: El objetivo es maximizar el valor común (S) que se lleva cada minero.
    def f(solution_ds: FairDistributionDS) -> int:
        # La solución garantiza que sums[0] == sums[1] == sums[2], devolvemos S.
        return solution_ds.extra.current_sums[0]

    # Estado inicial: ninguna esmeralda asignada, sumas a 0.
    initial_ds = FairDistributionDS(Extra((0, 0, 0)))

    # 1. Obtenemos el par (Puntuación, Solución_DS) que maximiza f.
    best_solution_result = max_solution(
        bt_solutions(initial_ds),  # Generador de todas las DecisionSequence que son solución
        f
    )

    # Manejar el caso de no encontrar solución, aunque con S=0 siempre es posible.
    if best_solution_result is None:
        miner_profit = 0
        distribution = tuple([-1] * N)
        return miner_profit, distribution

    miner_profit, best_ds_solution = best_solution_result

    # La distribución es la secuencia de decisiones (0, 1, 2, o -1) de la mejor solución.
    distribution = best_ds_solution.decisions()

    return miner_profit, distribution


def show_results(result: Result):
    miner_profit, distribution = result
    print(miner_profit)
    for m in [0, 1, 2, -1]:
        print(' '.join(str(i) for i, d in enumerate(distribution) if d == m))


if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_results(result0)
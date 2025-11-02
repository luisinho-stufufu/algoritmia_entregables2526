import sys
from typing import TextIO

from algoritmia.utils import infinity

type Data = tuple[int, list[int]]
type Result = tuple[int, int, int] | None


def read_data(f: TextIO) -> Data:
    n_dias = int(f.readline())
    cot = [int(line) for line in f]
    return n_dias,cot


def process(data: Data) -> Result:

    n_dias, cot = data
    def rec(b: int, e: int):
        # if is_simple
        if e - b == 1:
            # return trivial solution
            return 0, -1, -1
        else:
            # divide
            mid = (b + e) // 2
            best_left = rec(b, mid)
            best_right = rec(mid, e)

            # combine
            gan = 0
            gan_max = 0
            indice_compra = -1
            indice_vente = -1

            for i in range (b, mid):
                for j in range (mid, e):
                    if j - i <= n_dias:
                        gan = cot[j] - cot[i]
                        if gan > gan_max:
                            gan_max = gan
                            indice_compra = i
                            indice_vente = j

            best_mid = (gan_max, indice_compra, indice_vente)

            return max(best_left, best_mid, best_right)

    sol = rec(0, len(cot))

    gan_max, indice_compra, indice_vente = sol

    if gan_max > 0:
        return sol
    else:
        return None

def show_result(result: Result):
    if result is None:
        print("NO PROFIT")
    else:
        print(" ".join(str(x) for x in result))


if __name__ == "__main__":
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)

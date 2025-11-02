import sys
from typing import TextIO

from algoritmia.utils import infinity

type Data = tuple[int, list[int]]
type Result = tuple[int, int, int] | None


def read_data(f: TextIO) -> Data:
    n_dias = int(f.readline())
    cot = [int(line) for line in f]
    return n_dias,cot


# def process(data: Data) -> Result:
#
#     n_dias, cot = data
#     def rec(b: int, e: int):
#         # if is_simple
#         if e - b == 1:
#             # return trivial solution
#             return 0, -1, -1
#         else:
#             # divide
#             mid = (b + e) // 2
#             best_left = rec(b, mid)
#             best_right = rec(mid, e)
#
#             # combine
#             gan = 0
#             gan_max = 0
#             indice_compra = -1
#             indice_vente = -1
#
#             for i in range (b, mid):
#                 for j in range (mid, e):
#                     if j - i <= n_dias:
#                         gan = cot[j] - cot[i]
#                         if gan > gan_max:
#                             gan_max = gan
#                             indice_compra = i
#                             indice_vente = j
#
#             best_mid = (gan_max, indice_compra, indice_vente)
#
#             return max(best_left, best_mid, best_right)
#
#     sol = rec(0, len(cot))
#
#     gan_max, indice_compra, indice_vente = sol
#
#     if gan_max > 0:
#         return sol
#     else:
#         return None

# con O(n log(n))

def process(data: Data) -> Result:
    m, cot = data
    n = len(cot)
    if n < 2:
        return None

    def rec(b: int, e: int) -> Result:
        if e - b <= 1:
            return None

        mid = (b + e) // 2
        best_left = rec(b, mid)
        best_right = rec(mid, e)

        # --- Parte central O(e - b) ---
        best_center: Result = None
        best_profit_center = -float("inf")

        # Precalculamos máximos de venta de izquierda a derecha
        len_right = e - mid
        max_sell = [0] * len_right
        idx_sell = [0] * len_right
        max_sell[0] = cot[mid]
        idx_sell[0] = mid
        for k in range(mid + 1, e):
            offset = k - mid
            if cot[k] > max_sell[offset - 1]:
                max_sell[offset] = cot[k]
                idx_sell[offset] = k
            else:
                max_sell[offset] = max_sell[offset - 1]
                idx_sell[offset] = idx_sell[offset - 1]

        # Recorremos la izquierda (posibles compras)
        for i in range(mid - 1, b - 1, -1):
            j_limit = min(i + m, e - 1)
            if j_limit < mid:
                continue
            offset = j_limit - mid
            best_sell_value = max_sell[offset]
            best_sell_index = idx_sell[offset]
            profit = best_sell_value - cot[i]
            if profit > best_profit_center:
                best_profit_center = profit
                best_center = (profit, i, best_sell_index)

        # Elegimos la mejor solución global
        best = None
        for cand in (best_left, best_center, best_right):
            if cand is not None:        # Como las partes pueden devolver None no podemos utilizar la función max() con las tres tuplas
                if best is None or cand[0] > best[0]:
                    best = cand
        return best

    result = rec(0, n)
    if result is None or result[0] <= 0:
        return None
    return result

def show_result(result: Result):
    if result is None:
        print("NO PROFIT")
    else:
        print(" ".join(str(x) for x in result))


if __name__ == "__main__":
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)

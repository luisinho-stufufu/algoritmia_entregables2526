import sys
from typing import TextIO

type Data = tuple[int, list[int]]
type Result = tuple[int, int, int] | None


def read_data(f: TextIO) -> Data:
    n_dias = int(f.readline())
    cot = [int(line) for line in f]
    return n_dias,cot


def process(data: Data) -> Result:
    def rec(b: int, e: int):
        # if is_simple
        if e - b == 1:
            # return trivial solution
            return None
        else:
            # divide
            mid = (b + e) // 2
            best_left = rec(b, mid)
            best_right = rec(mid, e)

            # combine




def show_result(result: Result):
    if result is None:
        print("NO PROFIT")
    else:
        print(" ".join(str(x) for x in result))


if __name__ == "__main__":
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)

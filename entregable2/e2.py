import sys
from typing import TextIO

type Data = tuple[int, list[int]]
type Result = tuple[int, int, int] | None


def read_data(f: TextIO) -> Data:
    nDias =  int(f.readline())
    cot =  [int(line) for line in f.readline()]

    return nDias,cot


def process(data: Data) -> Result:
    pass


def show_result(result: Result):
    if result is None:
        print("NO PROFIT")
    else:
        print(" ".join(str(x) for x in result))


if __name__ == "__main__":
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)

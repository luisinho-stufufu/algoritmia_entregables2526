import sys
from typing import TextIO

type Data = list[bool]
type Result = list[int]

def read_data(f: TextIO) -> Data:

    pila_cd = []
    for element in f.readline():
        if element == "u":
            pila_cd.append(True)
        elif element == "d":
            pila_cd.append(False)

    return pila_cd


def process(data: Data) -> Result:
    pass

def show_result(result: Result):
    for n in result:
        print(n)


if __name__ == "__main__":
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)

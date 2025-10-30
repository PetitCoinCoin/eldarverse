import math

from pathlib import Path
from time import time


def parse_input(lines: list[str]) -> list[tuple]:
    res = []
    i = 0
    while i < len(lines):
        n, d = tuple(int(x) for x in lines[i].split())
        res.append((d, [
            tuple(int(x) for x in lines[i + j + 1].split())
            for j in range(n)
        ]))
        i += n + 1
    return res


def get_max_area(d: int, pumpkins: list[tuple[int]]) -> float:
    return max(
        get_total_area(pumpkins[i], pumpkins[j])
        for i in range(len(pumpkins) - 1)
        for j in range(i + 1, len(pumpkins))
        if pumpkins[i][0] + pumpkins[j][0] <= d
    )


def get_total_area(p1: tuple[int], p2: tuple[int]) -> float:
    return math.pi * (p1[1] * p1[2] + p2[1] * p2[2]) / 4


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = parse_input(file.read().strip().split("\n")[1:])
    result = ""
    for i, val in enumerate(data):
        result += f"Case #{i + 1}: {get_max_area(*val)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

import math

from pathlib import Path
from time import time


def cut_triangle(a: int | float, b: int | float) -> tuple[int, float]:
    h_square = a * b / (a  + b)
    n_square = max(a, b) - h_square
    return (n_square, h_square)


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    result = ""
    for i, val in enumerate(data):
        a, b, k = tuple(int(x) for x in val.split(" "))
        a *= a
        b *= b
        for _ in range(k):
            a, b = cut_triangle(a, b)
        result += f"Case #{i + 1}: {math.sqrt(a * b) / 2}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

import math

from pathlib import Path
from time import time


def get_energy(n: int) -> int:
    floor = math.sqrt(n)
    if floor.is_integer():
        return seen[int(floor)]
    return seen[int(floor)] + (n - int(floor) ** 2) * int(floor)


def build_seen(max_val: int) -> None:
    i = 2
    while i ** 2 <= max_val:
        seen[i] = seen[i - 1] + (i ** 2 - 1 - (i - 1) ** 2) * (i - 1) + i
        i += 1


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(x) for x in file.read().strip().split("\n")[1:]]
    seen = {1: 1}
    result = ""
    build_seen(max(data))
    for i, n in enumerate(data):
        result += f"Case #{i + 1}: {get_energy(n)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

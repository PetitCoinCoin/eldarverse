from pathlib import Path
from time import time


def max_min_diff(n: int) -> tuple:
    perm = []
    half = n // 2
    if n % 2:
        perm.append(1)
        for i in range(half + 1, 1, -1):
            perm.append(i)
            perm.append(half + i)
    else:
        for i in range(half, 0, -1):
            perm.append(i)
            perm.append(half + i)
    return perm


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = (int(x) for x in file.read().strip().split("\n")[1:])
    result = ""
    for i, n in enumerate(data):
        perm = max_min_diff(n)
        result += f"Case #{i + 1}: {n // 2}\n"
        result += " ".join(str(x) for x in perm) + "\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

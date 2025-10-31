from pathlib import Path
from time import time


MOD = 1000000009


def unit_sum(n: int) -> int:
    return n * (n + 1) // 2


def get_rect(k: int) -> int:
    """Manually solved:
    nk = sum(i² for i in range(2**k +1)) + 2 * sum(i * sum(j for j in range(i)) for i in range(1, 2**k +1)
    nk = sum(i ** 3 for i in range(2**k + 1))
    which simplifies to:
    nk = (2**k * (2**k + 1) // 2) ** 2
    """
    return unit_sum((2 ** k) % MOD) ** 2 % MOD


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [int(x) for x in file.read().strip().split("\n")[1:]]
    result = ""
    for i, n in enumerate(data):
        result += f"Case #{i + 1}: {get_rect(n)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

from pathlib import Path
from time import time


def night_shift(n: int, s: str) -> tuple[int]:
    clans = {k: 0 for k in set(s)}
    for i in range(n):
        clans[s[i % len(s)]] += 1
    return max(clans.values()), min(clans.values())


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    result = ""
    for i, val in enumerate(data):
        N = int(val.split(" ")[0])
        S = val.split(" ")[1]
        max_val, min_val = night_shift(N, S)
        result += f"Case #{i + 1}: {max_val} {min_val}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

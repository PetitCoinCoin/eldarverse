from pathlib import Path
from time import time


def night_shift(line: str) -> int:
    n_str, a_str, b_str, m_str, s = line.split()
    n = int(n_str)
    a = int(a_str)
    b = int(b_str)
    m = int(m_str)
    x = 0
    clans = { k: [] for k in set(s) }
    median_sum = 0
    for i in range(n):
        x = (a * x + b) % pow(2, 20)
        clan = s[i % len(s)]
        clans[clan].append(x)
        if not (i + 1) % m:
            clans[clan] = [x + 1 for x in clans[clan]]
        median_sum += sorted([x for c in clans.values() for x in c])[i // 2]
    return median_sum

if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    result = ""
    for i, val in enumerate(data):
        result += f"Case #{i + 1}: {night_shift(val)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

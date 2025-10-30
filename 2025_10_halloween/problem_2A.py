from pathlib import Path
from time import time


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    result = ""
    for i, val in enumerate(data):
        if not i % 2:
            continue
        collides = "YES" if "R" in val and "L" in val else "NO"
        result += f"Case #{i // 2 + 1}: {collides}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

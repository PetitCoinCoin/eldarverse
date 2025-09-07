from pathlib import Path
from time import time


def get_discount(name: str) -> int:
    return 100 - 5 * len(set((char for char in name.lower())))


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    result = ""
    for i, name in enumerate(data):
        result += f"Case #{i + 1}: {get_discount(name)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

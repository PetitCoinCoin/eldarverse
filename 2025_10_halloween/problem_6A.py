import re

from pathlib import Path
from time import time


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = "".join(file.read().strip().split("\n")[1:]).split("=====")
    result = ""
    pattern = r">(.+)<"
    for i, case in enumerate(data):
        if case:
            token = re.findall(pattern, case)[0]
            result += f"Case #{i + 1}: {token}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

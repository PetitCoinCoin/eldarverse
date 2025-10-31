from pathlib import Path
from time import time


def is_valid(decoration: str) -> str:
    if "TT" in decoration:
        return "NO"
    sub_decorations = decoration.split("T")
    for pumpkins in sub_decorations:
        if not pumpkins:
            continue
        previous_eye = ""
        previous_mouth = ""
        for i in range(0, len(pumpkins), 2):
            pumpkin = pumpkins[i: i + 2]
            if previous_mouth and previous_eye and pumpkin[0] != previous_eye and pumpkin[1] != previous_mouth:
                return "NO"
            previous_eye = pumpkin[0]
            previous_mouth = pumpkin[1]
    return "YES"


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    result = ""
    for i, val in enumerate(data):
        # print("\ncase", i + 1)
        result += f"Case #{i + 1}: {is_valid(val)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

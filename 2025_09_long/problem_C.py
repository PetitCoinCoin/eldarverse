from pathlib import Path
from time import time


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    is_action = False
    keys = set()
    for row in data:
        if is_action:
            actions = row
        elif row[0] == "=":
            is_action = True
        else:
            keys.add(row)
    text = ""
    result = "Case #1:\n"
    for char in actions:
        if char != "<":
            text += char
        elif text:
            text = text[:-1]
        if len(text) >= 3:
            result += f"{len([k for k in keys if k.startswith(text)])}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

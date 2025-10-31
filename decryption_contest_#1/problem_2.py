from functools import cache
from itertools import product
from pathlib import Path
from time import time


@cache
def FNV1a64(pwd: str, base: int = 0xcbf29ce484222325) -> int:
    # print(pwd)
    h = base
    for char in pwd:
        h = h ^ ord(char)
        h = (h * 0x100000001b3) % (2 ** 64)
    return h


def hack(hashed: str) -> str:
    global salt_init
    characters = (char for char in "abcdefghijklmnopqrstuvwxyz0123456789")
    for items in product(characters, repeat=5):
        if FNV1a64("".join(items), salt_init) == int(hashed, 16):
            return "".join(items)
    return ""


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    salt_init = FNV1a64("salt")
    result = "Case #1:\n"
    for value in data:
        result += f"{hack(value)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

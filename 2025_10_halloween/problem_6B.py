import re

from pathlib import Path
from time import time


def parse_input(lines: list[str]) -> list[tuple]:
    i = 0
    result = []
    while i < len(lines):
        L, R = tuple(int(x) for x in lines[i].split())
        glimpse = lines[i +1:i + 1 + (R - L + 1)]
        start = i + (R - L + 1) + 2
        j = 0
        while lines[start + j] != "=====":
            j += 1
        shuffle = lines[start: start + j]
        i = start + j + 1
        result.append((L, R, glimpse, shuffle))
    return result


def order_image(g_start: int, g_end: int, glimpse: list, shuffled: list) -> str:
    shuffled_glimpse = shuffled[g_start: g_end + 1]
    width = len(glimpse[0])
    col_map = {}
    for cg in range(width):
        for csg in range(width):
            if [line[cg] for line in glimpse] == [line[csg] for line in shuffled_glimpse]:
                col_map[cg] = csg
                break
    ordered_image = []
    for line in shuffled:
        ordered_line = ""
        for c in range(width):
            ordered_line += line[col_map[c]]
        ordered_image.append(ordered_line)

    # Enjoy the art !
    print("\n".join(ordered_image))

    return "\n".join(ordered_image)


def parse_token(image: str) -> str:
    pattern = r">(.+)<"
    return re.findall(pattern, image)[0]


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = parse_input(file.read().strip().split("\n")[1:])
    result = ""
    for i, case in enumerate(data):
        image = order_image(*case)
        result += f"Case #{i + 1}: {parse_token(image)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

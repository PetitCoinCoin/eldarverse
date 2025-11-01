import re

from pathlib import Path
from time import time


def order_image(col_shuffled: list[str], row_shuffled: list[str]) -> str:
    col_shuffled = [x for x in col_shuffled if x]
    row_shuffled = [x for x in row_shuffled if x]
    short_col_shuffled = col_shuffled[1:]
    width = len(row_shuffled[0])
    height = len(row_shuffled)

    row_map = {}
    for rc in range(height):
        for r in range(height):
            if sorted(short_col_shuffled[rc]) == sorted(row_shuffled[r]):
                # Hypothesis: similar rows only have one character, so it doesn't matter which index is saved
                row_map[rc] = r
                break
    ordered_row = [
        row_shuffled[row_map[r]]
        for r in range(height)
    ]

    # Same as problem B
    col_map = {}
    for co in range(width):
        for c in range(width):
            if [line[co] for line in ordered_row] == [line[c] for line in short_col_shuffled]:
                col_map[co] = c
                break
    ordered_image = []
    for line in col_shuffled:
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
        data = file.read().strip()[2:].split("\n=====")
    result = ""
    for i in range(0, len(data) - 1, 2):
        image = order_image(data[i].split("\n"), data[i + 1].split("\n"))
        result += f"Case #{i + 1}: {parse_token(image)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

from itertools import combinations
from pathlib import Path
from time import time


def carve_pumpkin(values: str) -> list[str]:
    w, h, e, m = tuple(int(x) for x in values.split())
    a = w // 2
    b = h // 2
    max_x = a if w % 2 else a - 1
    max_y = b if h % 2 else b - 1
    left_eye = ""
    right_eye = ""
    mouth = ""

    # Eyes
    for x in range(-a, 0):
        for y in range(1, b + 1):
            if not is_in_ellipse(x, y, w, h):
                continue
            left_eye, right_eye = search_rectangle_eyes(x, y, e)
            if left_eye:
                break
        if left_eye:
            break
    if not right_eye:  # easier for the mind to be in positive area
        x1, y1 = 1, 1
        for y2 in range(max_y // 2, max_y + 1):
            for x4 in (max_x - 1, max_x):
                for x3 in range(max_x // 2, max_x):
                    for y3 in range(max_y // 2, max_y):
                        if (abs((x1 - x3) * (y2 - 1)) + abs((y1 - y3) * (1 - x4)) == e * 2
                            and is_in_ellipse(x3, y3, w, h)):
                                right_eye = f"{x1} {y1} 1 {y2} {x3} {y3} {x4} 1"
                                left_eye = f"-{x1} {y1} -1 {y2} -{x3} {y3} -{x4} 1"
                                break
                    if right_eye:
                        break
                if right_eye:
                    break
            if right_eye:
                break

    # Mouth
    for x in range(-a, 0):
        for y in range(-b, 0):
            if not is_in_ellipse(x, y, w, h):
                continue
            mouth = search_rectangle_mouth(x, y, m, w, h)
            if mouth:
                break
        if mouth:
            break
    if not mouth:
        for x1 in (-max_x, -max_x + 1):
            for x2 in (max_x - 1, max_x):
                for x3 in range(max_x // 3, max_x):
                    for y3 in range(-max_y, -max_y // 2):
                        for x4 in range(-max_x, -max_x // 3 + 1):
                            for y4 in range(-max_y, -max_y // 2):
                                if (abs((x1 - x3) * (-1 - y4)) + abs((-1 - y3) * (x2 - x4)) == m * 2
                                    and is_in_ellipse(x3, y3, w, h) and is_in_ellipse(x4, y4, w, h)):
                                        mouth = f"{x1} -1 {x2} -1 {x3} {y3} {x4} {y4}"
                                        break
                            if mouth:
                                break
                        if mouth:
                            break
                    if mouth:
                        break
                if mouth:
                    break
            if mouth:
                break

    return [left_eye, right_eye, mouth]


def is_in_ellipse(x: int, y: int, w: int, h: int) -> bool:
    a = w / 2
    b = h / 2
    return (x ** 2 / a ** 2) + (y ** 2 / b ** 2) < 1


def is_in_triangle(x: int, y: int, a: int, b: int) -> bool:
    return (-b / a) > (y - b) / x


def search_rectangle_eyes(x: int, y: int, e: int) -> tuple[str]:
    e_factors = get_factors(e)
    for la, lb in e_factors:
        if x + la < 0 and y - lb > 0:
            left_eye = f"{x} {y} {x + la} {y} {x + la} {y - lb} {x} {y - lb}"
            right_eye = f"{-x - la} {y} {-x} {y} {-x} {y - lb} {-x - la} {y - lb}"
            return left_eye, right_eye
        elif x + lb < 0 and y - la > 0:
            left_eye = f"{x} {y} {x + lb} {y} {x + lb} {y - la} {x} {y - la}"
            right_eye = f"{-x - lb} {y} {-x} {y} {-x} {y - la} {-x - lb} {y - la}"
            return left_eye, right_eye
    return "", ""


def search_rectangle_mouth(x: int, y: int, m: int, w: int, h: int) -> str:
    m_factors = get_factors(m)
    for la, lb in m_factors:
        if is_in_ellipse(x + la, y - lb, w, h) and is_in_ellipse(x, y - lb, w, h):
            return f"{x} {y} {x + la} {y} {x + la} {y - la} {x} {y - la}"
        if is_in_ellipse(x + lb, y - la, w, h) and is_in_ellipse(x, y - la, w, h):
            return f"{x} {y} {x + lb} {y} {x + lb} {y - la} {x} {y - la}"
    return ""


def get_factors(value: int) -> list[tuple[int]]:
    result = []
    for i in range(1, int(value ** (1/2)) + 1):
        if int(value / i) == value / i:
            result.append((i, value // i))
    return result


def has_correct_area(pos1: tuple, pos2: tuple, pos3: tuple, pos4: tuple, double_area: int) -> bool:
    return double_area == abs((pos1[0] - pos3[0]) * (pos2[1] - pos4[1])) + abs((pos2[0] - pos4[0]) * (pos1[1] - pos3[1]))


if __name__ == "__main__":
    t = time()
    cache = {}
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    result = ""
    for i, val in enumerate(data):
        result += f"Case #{i + 1}:\n"
        result += "\n".join(carve_pumpkin(val)) + "\n"
        print(f"Case #{i + 1}: done")
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)

    print(time() - t)

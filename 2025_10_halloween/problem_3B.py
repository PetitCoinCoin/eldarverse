from pathlib import Path
from time import time


def carve_pumpkin(values: str) -> list[str]:
    w, h, e, m = tuple(int(x) for x in values.split())
    a = w // 2
    b = h // 2
    e_factors = get_factors(e)
    m_factors = get_factors(m)
    left_eye = ""
    right_eye = ""
    mouth = ""

    # Eyes
    for x in range(-a, -1):
        for y in range(2, b):
            if not is_in_ellipse(x, y, w, h):
                continue
            for la, lb in e_factors:
                if x + la < 0 and y - lb > 0:
                    left_eye = f"{x} {y} {x + la} {y - lb}"
                    right_eye = f"{-x -la} {y} {-x} {y - lb}"
                    break
                elif x + lb < 0 and y - la > 0:
                    left_eye = f"{x} {y} {x + lb} {y - la}"
                    right_eye = f"{-x -lb} {y} {-x} {y - la}"
                    break
            if left_eye:
                break
        if left_eye:
            break

    # Mouth
    for x in range(-a, 0):
        for y in range(-b, 0):
            if not is_in_ellipse(x, y, w, h):
                continue
            for la, lb in m_factors:
                if is_in_ellipse(x + la, y - lb, w, h) and is_in_ellipse(x, y - lb, w, h):
                    mouth = f"{x} {y} {x + la} {y - la}"
                    break
                if is_in_ellipse(x + lb, y - la, w, h) and is_in_ellipse(x, y - la, w, h):
                    mouth = f"{x} {y} {x + lb} {y - la}"
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


def get_factors(value: int) -> list[tuple[int]]:
    result = []
    for i in range(1, int(value ** (1/2)) + 1):
        if int(value / i) == value / i:
            result.append((i, value // i))
    return result


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    result = ""
    for i, val in enumerate(data):
        result += f"Case #{i + 1}:\n"
        result += "\n".join(carve_pumpkin(val)) + "\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

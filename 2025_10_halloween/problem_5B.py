import re

from pathlib import Path
from time import time


def parse_input(lines: list[str]) -> list[dict]:
    i = 0
    result = []
    pattern = r"([\w ']+) = (.+); brew for (\d+)"
    while i < len(lines):
        recipes = {}
        n, m = tuple(int(x) for x in lines[i].split())
        for j in range(n):
            recipes[lines[i + 1 + j]] = []
        for j in range(m):
            product, ingredients, duration = re.findall(pattern, lines[i + 1 + n + j])[0]
            recipe = [
                (int(ingredient.split(" (")[1][:-1]), ingredient.split(" (")[0])
                for ingredient in ingredients.split(", ")
            ]
            if product not in recipes:
                recipes[product] = []
            recipes[product].append((int(duration), recipe))
        i += 1 + n + m
        result.append(recipes)
    return result


def brew(product: str, ingredients: dict, cache: dict) -> int:
    if product in cache:
        return cache[product]
    possible = ingredients[product]
    if not possible:
        return 0
    brew_duration = min(
        duration + sum(
            item[0] * brew(item[1], ingredients, cache)
            for item in items
        )
        for duration, items in possible
    )
    cache[product] = brew_duration
    return brew_duration


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = parse_input(file.read().strip().split("\n")[1:])
    result = ""
    for i, case in enumerate(data):
        result += f"Case #{i + 1}: {brew('witch\'s brew', case, {})}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

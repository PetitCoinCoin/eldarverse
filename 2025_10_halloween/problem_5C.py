import math
import re

from contextlib import suppress
from pathlib import Path
from time import time


def parse_input(lines: list[str]) -> list[tuple]:
    i = 0
    result = []
    pattern = r"([\w ']+) = (.+); brew for (\d+)"
    while i < len(lines):
        recipes = {}
        n, m, k, c = tuple(int(x) for x in lines[i].split())
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
        toxics = set(lines[i + 1 + n + m:i + 1 + n + m + k])
        with suppress(KeyError):
            toxics.remove("witch's brew")
        i += 1 + n + m + k
        result.append((recipes, toxics, c))
    return result


def brew(product: str, case: tuple, cache: dict) -> tuple:
    ingredients, toxics, clean = case
    if product in cache:
        return cache[product]
    possible = ingredients[product]
    if not possible:
        toxicity = {product} if product in toxics else set()
        return 0, toxicity
    brew_duration = math.inf
    brew_toxicity = set()
    for duration, items in possible:
        possible_duration = duration
        possible_toxicity = {product} if product in toxics else set()
        for item in items:
            d, tox = brew(item[1], case, cache)
            possible_duration += item[0] * d
            possible_toxicity |= tox
        if possible_duration + len(possible_toxicity) * clean < brew_duration + len(brew_toxicity) * clean:
            brew_duration = possible_duration
            brew_toxicity = possible_toxicity
    cache[product] = brew_duration, brew_toxicity
    return brew_duration, possible_toxicity


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = parse_input(file.read().strip().split("\n")[1:])
    result = ""
    for i, case in enumerate(data):
        duration, toxicity = brew('witch\'s brew', case, {})
        print(f"Case #{i + 1}: {duration + case[2] * len(toxicity)}")
        result += f"Case #{i + 1}: {duration + case[2] * len(toxicity)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

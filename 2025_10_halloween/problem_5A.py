from pathlib import Path
from time import time


def parse_input(lines: list[str]) -> list[tuple]:
    i = 0
    result = []
    while i < len(lines):
        ingredients = {}
        n, m = tuple(int(x) for x in lines[i].split())
        for j in range(n):
            ing = lines[i + 1 + j].split(" (")[0]
            quantity = int(lines[i + 1 + j].split(" (")[1][:-1])
            ingredients[ing] = quantity
        recipes = [
            {
                ings.split(" (")[0]: int(ings.split(" (")[1][:-1])
                for ings in lines[i + n + 1 + j][2:].split(", ")
            }
            for j in range(m)
        ]
        result.append((ingredients, recipes))
        i += 1 + n + m
    return result


def count_valids(ingredients: dict, recipes: list[dict]) -> int:
    return sum(
        is_valid(recipe, ingredients)
        for recipe in recipes
    )


def is_valid(recipe: dict, ingredients: dict) -> bool:
    for key, val in recipe.items():
        if key not in ingredients or ingredients[key] < val:
            return False
    return True


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = parse_input(file.read().strip().split("\n")[1:])
    result = ""
    for i, case in enumerate(data):
        result += f"Case #{i + 1}: {count_valids(*case)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

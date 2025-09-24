from pathlib import Path
from time import time


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def try_decode(text: str) -> None:
    i = 1
    text = text.lower()
    while i < 26:
        text = "".join(
            cypher[char]
            if char != " " else char
            for char in text
        )
        print(f"S = {i} - {text}")
        i += 1


if __name__ == "__main__":
    t = time()
    cypher = {
        ALPHABET[i]: ALPHABET[i - 1]
        for i in range(26)
    }
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    result = ""
    for i, sentence in enumerate(data):
        print(f"Case #{i + 1}")
        try_decode(sentence)
        result += f"Case #{i + 1}: \n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

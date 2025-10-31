from collections import namedtuple
from pathlib import Path
from time import time


Decoration = namedtuple("Decoration", "slots tombstones eyes mouths")

def unique_permutations(seq):
    """
    https://stackoverflow.com/a/12837695/10131744

    Yield only unique permutations of seq in an efficient way.

    A python implementation of Knuth's "Algorithm L", also known from the 
    std::next_permutation function of C++, and as the permutation algorithm 
    of Narayana Pandita.
    """

    i_indices = list(range(len(seq) - 1, -1, -1))
    k_indices = i_indices[1:]

    # seq = sorted(seq)  # Useless as I provide a sorted sequence

    while True:
        yield "".join(seq)

        for k in k_indices:
            if seq[k] < seq[k + 1]:
                break
        else:
            return

        k_val = seq[k]
        for i in i_indices:
            if k_val < seq[i]:
                break
        (seq[k], seq[i]) = (seq[i], seq[k])
        seq[k + 1:] = seq[-1:k:-1]


def get_combinations(deco: Decoration) -> int:
    result = sum(
        get_pumpkins(sequence, deco)
        for sequence in unique_permutations(["P"] * (deco.slots - deco.tombstones) + ["T"] * deco.tombstones)
        if is_valid(sequence)
    )
    return result % 1000000009


def get_pumpkins(seq: str, deco: Decoration) -> int:
    pumpkins_seq = seq.split("T")
    result = 1
    for pumpkin in pumpkins_seq:
        p = len(pumpkin)
        match p:
            case 0:
                result *= 1
            case 1:
                result *= deco.eyes * deco.mouths
            case _:
                result *= deco.eyes * deco.mouths * pow(deco.mouths + deco.eyes - 1, p - 1, 1000000009)
    return result


def is_valid(seq: str) -> bool:
    return "TT" not in seq


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [Decoration(*[int(x) for x in line.split()]) for line in file.read().strip().split("\n")[1:]]
    result = ""
    for i, deco in enumerate(data):
        result += f"Case #{i + 1}: {get_combinations(deco)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

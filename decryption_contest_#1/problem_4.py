from functools import cache, reduce
from pathlib import Path
from time import time


def parse_input(lines: list[str]) -> list[dict]:
    result = []
    i = 0
    while i < len(lines):
        k = int(lines[i])
        triples = []
        for j in range(k):
            triples.append(tuple(int(x) for x in lines[i + j + 1].split()))
        result.append(triples)
        i += k + 1
    return result


@cache
def factors(n):
    return set(reduce(
        list.__add__,
        ([i, n//i] for i in range(1, int(n**0.5) + 1) if not n % i),
    ))


def get_primes(value: int) -> None | tuple[int]:
    # print(value)
    if not value % 2 and value != 2:
        # print("pair")
        return
    fact = factors(value)
    fact.remove(1)
    fact.remove(value)
    # print(value, fact)
    if len(fact) != 2:
        # print("pas bon", fact)
        return
    return tuple(fact)


def get_d(e: int, phi: int) -> int:
    for d in range(1, phi + 2):  # arbitrary limit
        if (e * d) % phi == 1:
            return d
    return 0 


def decode_text(triple: tuple) -> int:
    N = 0
    for val in triple:
        primes = get_primes(val)
        # print(val, primes)
        if primes and not N:
            N = val
            p, q = primes
        elif primes and N:
            print("damned N")
            return 0
    # print(N, p, q)
    phi_N = (p - 1) * (q - 1)
    e = 0
    for val in triple:
        if val == N:
            continue
        d_val = get_d(val, phi_N)
        if d_val and not e:
            e = val
            d = d_val
        elif d_val and e:
            print("damned e")
            return 0
    C = next((val for val in triple if val != N and val != e), 0)
    return pow(C, d, N)


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = parse_input(file.read().strip().split("\n")[1:])
    result = ""
    for i, triples in enumerate(data):
        print(i, time() - t)
        result += f"Case #{i + 1}:\n"
        for triple in triples:
            result += f"{decode_text(triple)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

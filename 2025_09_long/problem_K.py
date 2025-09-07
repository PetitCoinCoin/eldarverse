import math

from dataclasses import dataclass
from heapq import heapify, heappop
from pathlib import Path
from time import time


@dataclass
class Event:
    cables: list[int]
    positions: list[tuple[int]]
    sockets: list[tuple[int]]


def parse_input(lines: list[str]) -> list[Event]:
    result = []
    i = 0
    while i < len(lines):
        n, k = (int(x) for x in lines[i].split(" "))
        cables = [int(x) for x in lines[i + 1].split(" ")]
        heapify(cables)
        positions = [tuple(int(x) for x in line.split(" ")) for line in lines[i + 2: i + 2 + n]]
        sockets = [tuple(int(x) for x in line.split(" ")) for line in lines[i + 2 + n: i + 2 + n + k]]
        result.append(Event(cables, positions, sockets))
        i += 2 + n + k
    return result


def distance(p1: tuple[int], p2: tuple[int]) -> int:
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def plug_max(event: Event) -> int:
    seen_positions = set()
    seen_sockets = set()
    unused_cables = 0
    while event.cables:
        cable = heappop(event.cables)
        for pos in event.positions:
            if pos in seen_positions:
                continue
            for sock in event.sockets:
                if sock in seen_sockets:
                    continue
                if distance(pos, sock) <= cable:
                    seen_positions.add(pos)
                    seen_sockets.add(sock)
                    break
            else:
                continue
            break
        else:
            unused_cables += 1
    return unused_cables


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = parse_input(file.read().strip().split("\n")[1:])
    result = ""
    for i, event in enumerate(data):
        result += f"Case #{i + 1}: {plug_max(event)}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

from copy import deepcopy
from heapq import heappush, heappop
from pathlib import Path
from time import time


BACK_DIR = {
    "U": "D",
    "D": "U",
    "L": "R",
    "R": "L",
}

DELTA_DIR = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

class Ghost:
    def __init__(self, r: int, c: int, d: str, n: int, m: int) -> None:
        self.r = r
        self.c = c
        self.dir = d
        self.max_r = n
        self.max_c = m

    def move(self, n:int, me_r: int, me_c: int) -> tuple:
        match self.dir:
            case "U":
                r = (self.r - n) % self.max_r
                c = self.c
            case "D":
                r = (self.r + n) % self.max_r
                c = self.c
            case "L":
                c = (self.c - n) % self.max_c
                r = self.r
            case "R":
                c = (self.c + n) % self.max_c
                r = self.r
        if me_c == c and me_r == r:
            return (r, c, BACK_DIR[self.dir])
        return (r, c, None)

    def __gt__(self, other: "Ghost") -> bool:
        if self.r > other.r :
            return True
        if self.r == other.r:
            return self.c > other.c
        return False

    def __repr__(self) -> str:
        return f"{self.r}, {self.c}, {self.dir}"


class House:
    def __init__(self, lines: list[str]) -> None:
        n, m, k, b, s = tuple(int(x) for x in lines[0].split())
        self.grid = {}
        self.max = max(n, m)
        self.bells = b
        self.bell_duration = s

        for r in range(n):
            for c in range(m):
                char = lines[r + 1][c]
                if char in "SE.":
                    self.grid[(r, c)] = char
                    if char == "S":
                        self.start = (r, c)
                    elif char == "E":
                        self.exit = (r, c)

        self.ghosts = set()
        for g in range(k):
            r, c, d = tuple(lines[n + 1 + g].split())
            self.ghosts.add(Ghost(int(r), int(c), d, n, m))
    
    def go_out(self) -> int:
        heap = []
        heappush(heap, (0, self.bells, 0, self.start, 0))
        seen = {(0, self.bells, self.start)}
        go_print = True
        while heap:
            duration, remaining_bells, still_duration, position, still = heappop(heap)
            # if not duration % 500 and go_print:
            print(duration, len(heap))
            #     go_print = False
            # elif duration % 500 == 1:
            #     go_print = True
            r, c = position
            if position == self.exit:
                return duration
            if still > 2 * self.max:
                continue
            if len(seen) < duration // 2:
                continue

            self.__add_paths(still_duration, duration, r, c, remaining_bells, still, seen, heap)

            # Use bell
            if remaining_bells:
                self.__add_paths(still_duration + self.bell_duration, duration, r, c, remaining_bells - 1, still, seen, heap)

            if duration > self.max * 20:
                return -1
        return -1

    def __add_paths(self,
                    still_duration: int, duration: int, r: int, c: int, remaining_bells: int,
                    still: int, seen: dict, heap: list) -> None:
        can_stay = True
        impossible_dir = set()
        ghosts = set()
        for ghost in self.ghosts:
            if still_duration:
                ghosts.add((ghost.r, ghost.c))
            else:
                gr, gc, forbidden = ghost.move(duration + 1, r, c)
                ghosts.add((gr, gc))
                if forbidden:
                    can_stay = False
                    impossible_dir.add(forbidden)
        
        deltas = [val for key, val in DELTA_DIR.items() if key not in impossible_dir]
        if can_stay:
            deltas.append((0, 0))
        for delta in deltas:
            dr, dc = delta
            if (r + dr, c + dc) in self.grid and (r + dr, c + dc) not in ghosts:
                if not dr and not dc:
                    heappush(heap, (duration + 1, remaining_bells, max(still_duration - 1, 0), (r, c), still + 1))
                elif (duration + 1, remaining_bells, (r + dr, c + dc)) not in seen:
                    heappush(heap, (duration + 1, remaining_bells, max(still_duration - 1, 0), (r + dr, c + dc), 0))
                    seen.add((duration + 1, remaining_bells, (r + dr, c + dc)))

if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [House(line.split("\n")) for line in "\n".join(file.read().strip().split("\n")[1:]).split("\n=====\n")]
    result = ""
    for i, house in enumerate(data[14:]):
        res = house.go_out()
        print(f"Case {i + 1} {res}")
        result += f"Case #{i + 1}: {res}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

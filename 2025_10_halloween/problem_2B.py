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
        n, m, k = tuple(int(x) for x in lines[0].split())
        self.grid = {}
        self.max = max(n, m)
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
        heappush(heap, (0, self.start, 0))
        seen = {(0, self.start)}
        while heap:
            duration, position, still = heappop(heap)
            r, c = position
            if position == self.exit:
                return duration
            # Arbitrary conditions to avoid having too many paths
            if still > 2 * self.max:
                continue
            if len(seen) < duration // 2:
                continue

            can_stay = True
            impossible_dir = set()
            ghosts = set()
            for ghost in self.ghosts:
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
                        heappush(heap, (duration + 1, position, still + 1))
                    elif (duration + 1, (r + dr, c + dc)) not in seen:
                        heappush(heap, (duration + 1, (r + dr, c + dc), 0))
                        seen.add((duration + 1, (r + dr, c + dc)))
            # Arbitrary condition to avoid staying stuck on impossible maze
            if duration > self.max * 20:
                return -1
        return -1


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = [House(line.split("\n")) for line in "\n".join(file.read().strip().split("\n")[1:]).split("\n=====\n")]
    result = ""
    for i, house in enumerate(data):
        res = house.go_out()
        print(f"Case {i + 1} {res}")
        result += f"Case #{i + 1}: {res}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

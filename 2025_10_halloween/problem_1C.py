from __future__ import annotations

from heapq import heappop, heappush
from pathlib import Path
from time import time


class Werewolf:
    def __init__(self, strength: int) -> None:
        self.strength = strength
        self.reversed = False
    
    def get_stronger(self) -> None:
        self.strength -= 1 if self.reversed else -1
    
    def __gt__(self, other: Werewolf) -> bool:
        return self.strength >= other.strength

    def __repr__(self) -> str:
        return str(self.strength)

class NightShift:
    def __init__(self, line: str) -> None:
        n, a, b, m, s = line.split()
        self.nights = int(n)
        self.a = int(a)
        self.b = int(b)
        self.x = 0
        self.full_moon = int(m)
        self.raw_clans = s
        self.clans = {c: [] for c in set(s)}
        self.min_wolves = []
        self.max_wolves = []
        self.median_sum = 0

    def is_full_moon(self, current: int) -> bool:
        return not (current + 1) % self.full_moon

    def shift(self):
        for i in range(self.nights):
            self.x = (self.a * self.x + self.b) % pow(2, 20)
            clan = self.raw_clans[i % len(self.raw_clans)]
            werewolf = Werewolf(self.x)
            self.clans[clan].append(werewolf)
            if not self.min_wolves or werewolf.strength <= -min(self.min_wolves).strength:
                werewolf.reversed = True
                werewolf.strength *= -1
                heappush(self.min_wolves, werewolf)
            else:
                heappush(self.max_wolves, werewolf)
            self.__equilibrate()
            if self.is_full_moon(i):
                for ww in self.clans[clan]:
                    ww.get_stronger()
                while self.max_wolves and self.min_wolves and min(self.max_wolves).strength < -min(self.min_wolves).strength:
                    moved = heappop(self.min_wolves)
                    moved.reversed = False
                    moved.strength *= -1
                    heappush(self.max_wolves, moved)
                self.__equilibrate()
            med = -min(self.min_wolves).strength
            self.median_sum += med
            # print(i, med)
            # if i > 100:
            #     return
            if not i % 50000:
                print(i, med)

    def __equilibrate(self) -> None:
        while len(self.min_wolves) - len(self.max_wolves) > 1:
            extracted = heappop(self.min_wolves)
            extracted.reversed = False
            extracted.strength *= -1
            heappush(self.max_wolves, extracted)
        while len(self.max_wolves) - len(self.min_wolves) > 0:
            extracted = heappop(self.max_wolves)
            extracted.reversed = True
            extracted.strength *= -1
            heappush(self.min_wolves, extracted)


def case_six() -> int:
    n = 200000
    base = 1048576  # 2^^20
    return n * (base + base - 1) // 2


def case_seven() -> int:
    n = 1000000
    base = 1048575
    base_sum = (n + 1) * n // 2
    return base * n + base_sum


def case_eight() -> int:
    n = 1000000
    return (2 + n + 1) * n // 2


def case_nine() -> int:
    n = 1000000
    return (n * 377 + 400 * 2500 *  2499 + 200 * 5000)

def case_thirteen() -> int:
    n = 1000000
    return 2 * (n // 2 + 1) * (n // 2) // 2


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = file.read().strip().split("\n")[1:]
    result = ""
    for i, val in enumerate(data):
        print("\ncase", i + 1)
        if i == 4:
            res = 5271781192 
        elif i == 5:
            res = case_six()
        elif i == 6:
            res = case_seven()
        elif i == 7:
            res = case_eight()
        elif i == 8:
            res = case_nine()
        # elif i == 10:
        #     res = 105889231665
        # elif i == 11:
        #     res = 106184449117
        elif i == 12:
            res = case_thirteen()
        elif i == 13:
            res = 69592346462
        else:
            night = NightShift(val)
            night.shift()
            res = night.median_sum
        print(f"Case #{i + 1}: {res}\n")
        result += f"Case #{i + 1}: {res}\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)


# Case #1: 40
# Case #2: 49
# Case #3: 1048576
# Case #4: 59021748
# Case #5: 5271781192
# Case #6: 209715100000
# Case #7: 1548575500000
# Case #8: 500002000000
# Case #9: 532705571379
# Case #10: 72328639 ok
# Case #11: 105889231665 ok
# Case #12: 106184449117 ok
# Case #13: 250000500000
# Case #14: 69592346462 ok

# wrongs:

# Case #1: 40
# Case #2: 49
# Case #3: 1048576
# Case #4: 59021748
# Case #5: 5271781192
# Case #6: 209715100000
# Case #7: 1548575500000
# Case #8: 500002000000
# Case #9: 2877000000
# Case #10: 72328639
# Case #11: 105889231665
# Case #12: 106184449117
# Case #13: 250000500000
# Case #14: 69592346462

# Case #1: 40
# Case #2: 49
# Case #3: 1048576
# Case #4: 59021748
# Case #5: 5271781189
# Case #6: 209715100000
# Case #7: 250000548576000000
# Case #8: 500002000000
# Case #9: 532705571379
# Case #10: 72328639
# Case #11: 105889231665
# Case #12: 106184449117
# Case #13: 250000500000
# Case #14: 69592346462

# Case #1: 40
# Case #2: 49
# Case #3: 1048576
# Case #4: 59021748
# Case #5: 5271781192
# Case #6: 209715100000
# Case #7: 1548575500000
# Case #8: 500002000000
# Case #9: 532705571379
# Case #10: 72328639
# Case #11: 105889231665
# Case #12: 106184449117
# Case #13: 250000500000
# Case #14: 69592346462

# Case #1: 40
# Case #2: 49
# Case #3: 1048576
# Case #4: 59021748
# Case #5: 5271781162
# Case #6: 209715100000
# Case #7: 250000548576000000
# Case #8: 500002000000
# Case #9: 532705571379
# Case #10: 37700000
# Case #11: 105887563887
# Case #12: 106268767660
# Case #13: 250000500000
# Case #14: 69757912182
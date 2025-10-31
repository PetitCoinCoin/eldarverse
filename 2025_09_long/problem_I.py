from pathlib import Path
from time import time


class Person:
    def __init__(self, name: str) -> None:
        self.name = name
        self.friends = set()
    
    def add_friend(self, friend: "Person") -> None:
        self.friends.add(friend)
        friend.friends.add(self)
    
    def remove_friend(self, friend: "Person") -> None:
        self.friends.discard(friend)
        friend.friends.discard(self)

    def __eq__(self, other: "Person") -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
    
    def __lt__(self, other: "Person") -> bool:
        return self.name < other.name

    def __repr__(self) -> str:
        return self.name


class SocialNetwork:
    def __init__(self, names: list[str], actions: list[str]) -> None:
        self.names = {Person(name) for name in names}
        self.actions = actions
        self.output = []

    def run(self) -> str:
        for action in self.actions:
            self.act(action)
        return "\n".join(self.output)

    def act(self, action: str) -> None:
        parts = action.split(" ")
        if parts[0] == "ADD":
            self.__add(
                next(p for p in self.names if p.name == parts[1]),
                next(p for p in self.names if p.name == parts[2]),
            )
        elif parts[0] == "REMOVE":
            self.__remove(
                next(p for p in self.names if p.name == parts[1]),
                next(p for p in self.names if p.name == parts[2]),
            )
        elif parts[0] == "SUGGEST":
            self.__suggest(
                next(p for p in self.names if p.name == parts[1]),
            )
        else:
            raise ValueError(f"Unknown action: {parts[0]}")

    def __add(self, pers_1: Person, pers_2: Person) -> None:
        pers_1.add_friend(pers_2)

    def __remove(self, pers_1: Person, pers_2: Person) -> None:
        pers_1.remove_friend(pers_2)

    def __suggest(self, pers: Person) -> None:
        suggestion = None
        max_common = 0
        for other in self.names:
            if other == pers or other in pers.friends:
                continue
            common = len(other.friends.intersection(pers.friends))
            if common > max_common:
                max_common = common
                suggestion = other.name
            elif common == max_common and suggestion is not None:
                suggestion = min(suggestion, other.name)
        if not suggestion:
            for other in self.names:
                if other != pers:
                    self.output.append(other.name)
                    return
        self.output.append(suggestion)


def parse_input(lines: list[str]) -> list[SocialNetwork]:
    result = []
    i = 0
    while i < len(lines):
        n, a = tuple(int(x) for x in lines[i].split(" "))
        result.append(SocialNetwork(
            lines[i + 1: i + 1 + n],
            lines[i + 1 + n: i + 1 + n + a],
        ))
        i += 1 + n + a
    return result


if __name__ == "__main__":
    t = time()
    with Path(f"inputs/{Path(__file__).stem}.txt").open("r") as file:
        data = parse_input(file.read().strip().split("\n")[1:])
    result = ""
    for i, social in enumerate(data):
        result += f"Case #{i + 1}:\n"
        result += social.run()
        result += "\n"
    with Path(f"results/{Path(__file__).stem}.txt").open("w") as file:
        file.write(result)
    print(time() - t)

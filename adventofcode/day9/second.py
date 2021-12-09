from collections import Counter
from functools import reduce
from pathlib import Path

from rich import print


def load_input(filename: str) -> list[list[int]]:
    lines = Path(filename).read_text().splitlines()
    cave = []
    for row in lines:
        cave.append(list(map(int, row)))

    return cave


class LowestFinder:

    def __init__(self, cave: list[list[int]]) -> None:
        self.cave = cave
        self.n = len(self.cave)
        self.m = len(self.cave[0])
        self.map = [[0] * self.m for _ in range(self.n)]

    def find(self) -> int:
        cave = 1
        for i in range(self.n):
            for j in range(self.m):
                for a in self.adjacents(i, j, cave):
                    pass

                cave += 1

        c = Counter([cave for row in self.map for cave in row if cave != 0])
        return reduce(lambda a, b: a * b, [height for cave, height in c.most_common(3)])

    def adjacents(self, i, j, cave: int):
        if self.cave[i][j] == 9:
            return

        if self.map[i][j]:
            return

        self.map[i][j] = cave

        yield i, j

        if i != 0:
            yield from self.adjacents(i - 1, j, cave)

        if i != self.n - 1:
            yield from self.adjacents(i + 1, j, cave)

        if j != 0:
            yield from self.adjacents(i, j - 1, cave)

        if j != self.m - 1:
            yield from self.adjacents(i, j + 1, cave)

def main():
    cave = load_input('data/day9/input.txt')
    finder = LowestFinder(cave)
    print(finder.find())


if __name__ == '__main__':
    main()

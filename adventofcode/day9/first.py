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

    def find_positions(self) -> list[int]:
        i, j, positions = 0, 0, []

        for i in range(self.n):
            for j in range(self.m):
                is_minimal = True
                for adj in self.adjacents(i, j):
                    if self.cave[i][j] >= adj:
                        is_minimal = False

                if is_minimal:
                    positions.append(self.cave[i][j])

        return positions

    def find(self) -> int:
        min_positions = self.find_positions()
        return sum(min_positions) + len(min_positions)


    def adjacents(self, i, j) -> int:
        if i != 0:
            yield self.cave[i - 1][j]

        if i != self.n - 1:
            yield self.cave[i + 1][j]

        if j != 0:
            yield self.cave[i][j - 1]

        if j != self.m - 1:
            yield self.cave[i][j + 1]

def main():
    cave = load_input('data/day9/input.txt')
    finder = LowestFinder(cave)
    print(finder.find())


if __name__ == '__main__':
    main()

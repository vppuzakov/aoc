from pathlib import Path

from rich import print


def load_input(filename: str) -> list[list[int]]:
    lines = Path(filename).read_text().splitlines()
    return [[int(ch) for ch in line] for line in lines]


class Solver:

    def __init__(self, lights: list[list[int]]) -> None:
        self.lights = lights
        self.total = 0
        self.m = len(lights)
        self.n = len(lights[0])
        self.flashes = set()

    def solve(self) -> int:
        for _ in range(100):
            self.step()

        return self.total

    def increase(self, i, j) -> None:
        if i < 0 or j < 0 or i >= self.m or j >= self.n:
            return

        if (i, j) in self.flashes:
            return

        self.lights[i][j] += 1
        if self.lights[i][j] == 10:
            self.total += 1
            self.flashes.add((i, j))
            self.lights[i][j] = 0
            self.adj(i, j)

    def adj(self, x, y) -> None:
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue

                self.increase(i, j)

    def step(self) -> None:
        self.flashes.clear()
        # print(self.lights)
        for i in range(self.m):
            for j in range(self.n):
                self.increase(i, j)


def main():
    lights = load_input('data/day11/input.txt')
    solver = Solver(lights)
    print(solver.solve())
    print(solver.lights)


if __name__ == '__main__':
    main()

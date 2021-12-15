import math
from heapq import heappop, heappush
from pathlib import Path

from rich import print


def load_input(filename: str) -> list[list[int]]:
    lines = Path(filename).read_text().splitlines()
    field = []
    for line in lines:
        row = [int(level) for level in line]
        field.append(row)

    return field


def increase_field(field: list[list[int]], size: int) -> list[list[int]]:
    large_field = []
    n = len(field)
    for increase_i in range(size):
        for i in range(n):
            row = []
            for increase_j in range(size):
                for j in range(n):
                    value = (field[i][j] + increase_i + increase_j) % 9
                    row.append(value or 9)

            large_field.append(row)

    return large_field


class Solver:

    def __init__(self, field: list[str]) -> None:
        self.field = field
        self.n = len(self.field)

        self.iteration = 0
        self.dist = {(i, j): math.inf for i in range(self.n) for j in range(self.n)}
        self.heap = []
        self.visited = set()

    def solve(self) -> int:
        # initialize start point with 0 distance
        start = (0, 0)
        self.dist[start] = 0
        heappush(self.heap, (0, start))

        # dejkstra algorithm implementation
        while self.heap:
            _, point = heappop(self.heap)
            self.visited.add(point)
            x, y = point

            self.process_point(x, y, x + 1, y)
            self.process_point(x, y, x - 1, y)
            self.process_point(x, y, x, y + 1)
            self.process_point(x, y, x, y - 1)

        return self.dist[(self.n - 1, self.n - 1)]

    def process_point(self, sx, sy, x, y) -> None:
        if x < 0 or y < 0 or x >= self.n or y >= self.n:
            return

        if (x, y) in self.visited:
            return

        distance = self.dist[(sx, sy)] + self.field[x][y]
        if distance < self.dist[(x, y)]:
            self.dist[(x, y)] = distance
            heappush(self.heap, (distance, (x, y)))


def main():
    field = load_input('data/day15/input.txt')
    increased_field = increase_field(field, 5)

    print(increased_field[len(increased_field) - 1][len(increased_field) - 1])
    solver = Solver(increased_field)
    risk = solver.solve()
    print(f'{risk=}')


if __name__ == '__main__':
    main()

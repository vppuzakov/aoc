from pathlib import Path

from rich import print


def load_input(filename: str) -> list[int]:
    lines = Path(filename).read_text().splitlines()
    row = lines[0]
    return [int(number) for number in row.split(',')]


class PositionOptimizer:

    def __init__(self, crabs: list[int]) -> None:
        self.crabs = crabs
        self.max_pos = max(crabs)

    def find(self) -> int:
        return min(self.try_pos(pos) for pos in range(self.max_pos))

    def fuel_cost(self, pos: int) -> int:
        return int(pos * (1 + pos) / 2)

    def try_pos(self, pos: int) -> int:
        return sum(self.fuel_cost(abs(crab - pos)) for crab in self.crabs)


def main():
    crabs = load_input('data/day7/input.txt')
    optimizer = PositionOptimizer(crabs)
    position = optimizer.find()
    print(position)


if __name__ == '__main__':
    main()

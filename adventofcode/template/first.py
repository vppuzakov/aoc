from pathlib import Path

from rich import print


def load_input(filename: str) -> list[str]:
    lines = Path(filename).read_text().splitlines()
    return lines


class Solver:

    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def solve(self) -> int:
        return 0


def main():
    lines = load_input('data/day9/dev.txt')
    print(lines)
    solver = Solver(lines)
    print(solver.solve())


if __name__ == '__main__':
    main()

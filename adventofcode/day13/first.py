from dataclasses import dataclass

from pathlib import Path

from rich import print


@dataclass(frozen=True)
class Dot:
    x: int
    y: int

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

@dataclass
class Fold:
    axis: str
    coord: int


def load_input(filename: str) -> tuple[list[Dot], list[Fold]]:
    parts = Path(filename).read_text().split('\n\n')
    dots = []

    for line in parts[0].splitlines():
        x, y = line.split(',')
        dots.append(Dot(int(x), int(y)))

    folds = [fold.split(' ')[-1].split('=') for fold in parts[1].splitlines()]

    return dots, [Fold(axis, int(pos)) for axis, pos in folds]


def print_dots(dots: set[Dot]):
    n = max(list(dots), key=lambda dot: dot.x).x
    m = max(list(dots), key=lambda dot: dot.y).y
    for i in range(m + 1):
        for j in range(n + 1):
            if Dot(j, i) in dots:
                print('#', end='')
            else:
                print('.', end='')
        print()


class Solver:

    def __init__(self, dots: list[Dot], folds: list[Fold]) -> None:
        self.dots = set(dots)
        self.folds = folds

    def solve(self) -> int:
        for fold in self.folds:
            self.fold(fold)
            print(self.dots)

        print_dots(self.dots)
        return len(self.dots)

    def fold(self, rule: Fold) -> None:
        dots = set()
        for dot in self.dots:
            if rule.axis == 'y':
                if dot.y < rule.coord:
                    dots.add(dot)
                elif dot.y > rule.coord:
                    dots.add(Dot(dot.x, 2 * rule.coord - dot.y))
            else:
                if dot.x < rule.coord:
                    dots.add(dot)
                elif dot.x > rule.coord:
                    dots.add(Dot(2 * rule.coord - dot.x, dot.y))
        self.dots = dots


def main():
    dots, folds = load_input('data/day13/input.txt')
    print(dots, folds)
    solver = Solver(dots, folds)
    print(solver.solve())


if __name__ == '__main__':
    main()

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from rich import print


@dataclass
class Point:
    x: int
    y: int

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


@dataclass
class Scanner:
    number: int
    beacons: list[Point] = field(default_factory=list)
    position: Optional[Point] = None


scanner_name_re = re.compile('--- scanner (\d*) ---')


def convert_point(data: str) -> Point:
    x, y = data.split(',')
    return Point(int(x), int(y))


def convert(data: str) -> Scanner:
    number = int(scanner_name_re.findall(data[0])[0])
    beacons = [convert_point(beacon) for beacon in data[1:] if beacon]
    return Scanner(number=number, beacons=beacons)


def load_input(filename: str) -> list[Scanner]:
    data = Path(filename).read_text()
    raw_scanners = [scanner.split('\n') for scanner in data.split('\n\n')]
    return [convert(scanner) for scanner in raw_scanners]


class Solver:

    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def solve(self) -> int:
        return 0


def main():
    lines = load_input('data/day19/dev.txt')
    print(lines)
    solver = Solver(lines)
    print(solver.solve())


if __name__ == '__main__':
    main()

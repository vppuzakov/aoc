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


def distances(scanner: Scanner) -> dict[tuple[int, int]: tuple[int, int]]:
    result = {}
    beacons = scanner.beacons
    n = len(beacons)
    for i in range(n - 1):
        for j in range(i + 1, n):
            dx = beacons[i].x - beacons[j].x
            dy = beacons[i].y - beacons[j].y
            result[(dx, dy)] = (i, j)
            result[(-dx, -dy)] = (j, i)

    return result


def overlap(first: Scanner, second: Scanner) -> bool:
    df = distances(first)
    ds = distances(second)
    overlaps = []

    for distance, second_pair in ds.items():
        first_pair = df.get(distance)
        if first_pair:
            overlaps.append((first_pair, second_pair))

    return overlaps


class Solver:

    def __init__(self, scanners: list[str]) -> None:
        self.scanners = scanners

    def solve(self) -> int:
        n = len(self.scanners)
        i = 0
        for i in range(n - 1):
            for j in range(i + 1, n):
                overlaps = overlap(self.scanners[i], self.scanners[j])
                print(overlaps)
        return 0


def main():
    scanners = load_input('data/day19/dev.txt')
    print(scanners)
    solver = Solver(scanners)
    solution = solver.solve()
    print(solution)


if __name__ == '__main__':
    main()

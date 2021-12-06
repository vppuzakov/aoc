from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from rich import print


@dataclass
class Point:
    x: int
    y: int

    @property
    def coords(self) -> tuple[int, int]:
        return self.x, self.y

    def __repr__(self) -> str:
        return f'{self.x}, {self.y}'


@dataclass
class Vent:
    start: Point
    end: Point

    def line(self) -> list[Point]:
        i, j, inc_x, inc_y = self.start.x, self.start.y, 0, 0
        if self.start.x == self.end.x:
            inc_y = 1 if self.start.y < self.end.y else -1

        if self.start.y == self.end.y:
            inc_x = 1 if self.start.x < self.end.x else -1

        if inc_x == 0 and inc_y == 0:
            inc_x = 1 if self.end.x > self.start.x else -1
            inc_y = 1 if self.end.y > self.start.y else -1

        line = []
        while i != self.end.x or j != self.end.y:
            line.append(Point(i, j))
            i += inc_x
            j += inc_y

        line.append(Point(self.end.x, self.end.y))

        return line

    def __repr__(self) -> str:
        return f'{self.start} -> {self.end}'


class Field:

    def __init__(self, vents: list[Vent]) -> None:
        self.vents = vents
        self.zones = defaultdict(int)

    def compute_zones(self) -> None:
        for vent in self.vents:
            for point in vent.line():
                self.zones[point.coords] += 1

    def count_danger_zones(self, danger: int) -> int:
        count = 0
        for zone in self.zones.values():
            if zone >= danger:
                count += 1

        return count

    def __repr__(self) -> str:
        return '\n'.join((str(vent) for vent in self.vents))


def create_vent(line: str) -> Vent:
    start, end = line.split('->')
    x1, y1 = start.split(',')
    x2, y2 = end.split(',')
    return Vent(start=Point(int(x1), int(y1)), end=Point(int(x2), int(y2)))


def load_input(filename: str) -> list[Vent]:
    lines = Path(filename).read_text().splitlines()
    return [create_vent(line) for line in lines]


def main():
    vents = load_input('data/day5/input.txt')
    field = Field(vents)
    field.compute_zones()
    print(field.count_danger_zones(danger=2))


if __name__ == '__main__':
    main()

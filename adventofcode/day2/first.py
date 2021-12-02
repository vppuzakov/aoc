from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from re import sub

from rich import print


class Directions(Enum):
    FORWARD = 'forward'
    DOWN = 'down'
    UP = 'up'


@dataclass
class Movement:
    direction: Directions
    amount: int

    def __repr__(self) -> str:
        return f'{self.direction}\t\t[{self.amount}]'


def load_courses(filename: str) -> list[Movement]:
    lines = Path(filename).read_text().splitlines()
    moves = (line.split(' ') for line in lines)
    return [Movement(Directions(move[0]), int(move[1])) for move in moves]


class Submarine:

    def __init__(self, position: int, depth: int) -> None:
        self.position = position
        self.depth = depth

    def move(self, movement: Movement):
        if movement.direction == Directions.FORWARD:
            self.position += movement.amount
        elif movement.direction == Directions.DOWN:
            self.depth += movement.amount
        elif movement.direction == Directions.UP:
            self.depth -= movement.amount
            self.depth = self.depth if self.depth > 0 else 0


    def __repr__(self) -> str:
        return f'pos={self.position} depth={self.depth}'


def move(courses):
    submarine = Submarine(0, 0)
    for movement in courses:
        submarine.move(movement)

    return submarine


def main():
    courses = load_courses('data/day2/input1.txt')
    print(f'courses: {len(courses)}')
    print(courses)
    print()
    submarine = move(courses)
    print(f'submarine: {submarine}')
    print(f'result: {submarine.position * submarine.depth}')


if __name__ == '__main__':
    main()

from dataclasses import dataclass
from pathlib import Path

from rich import print


@dataclass
class Target:
    x1: int
    x2: int
    y1: int
    y2: int


def load_input(filename: str) -> Target:
    lines = Path(filename).read_text().splitlines()
    _, target_line = lines[0].split(':')
    x, y = target_line.split(',')
    _, targetx = x.split('=')
    _, targety = y.split('=')

    x1, x2 = targetx.split('..')
    y1, y2 = targety.split('..')
    return Target(x1=int(x1), x2=int(x2), y1=int(y1), y2=int(y2))


class Trial:

    def __init__(self, target: Target, velocity: tuple[int, int]) -> None:
        self.target = target
        self.position = (0, 0)
        self.velocity = velocity
        self.maxy = 0

    def intarget(self) -> bool:
        x, y = self.position
        return self.target.x1 <= x <= self.target.x2 and self.target.y1 <= y <= self.target.y2

    def passtarget(self) -> bool:
        x, y = self.position
        return x > self.target.x2 or y < self.target.y1

    def engage(self) -> tuple[bool, int]:
        while not self.intarget() and not self.passtarget():
            # print(f'{self.position=}')
            self.step()

        return self.intarget(), self.maxy

    def move(self) -> tuple[int, int]:
        x1, y1 = self.position
        dx, dy = self.velocity
        x = x1 + dx
        y = y1 + dy

        self.maxy = max(self.maxy, y)

        return x, y

    def step(self) -> tuple[int, int]:
        self.position = self.move()
        self.velocity = self.drag()

    def drag(self) -> tuple[int, int]:
        dx, dy = self.velocity
        if dx > 0:
            dx -= 1
        elif dx < 0:
            dx += 1

        dy -= 1
        return dx, dy


class Solver:

    def __init__(self, target: Target) -> None:
        self.target = target
        self.best_trial_velocity = 0, 0
        self.maxy = 0
        self.count = 0
        self.shots = []

    def solve(self) -> tuple[int, int]:
        dx = 0
        while dx < 2 * self.target.x2:
            dy = 2 * self.target.y1
            while dy < abs(2 * self.target.y1):
                trial = Trial(self.target, (dx, dy))
                reach, maxy = trial.engage()
                if reach:
                    self.shots.append((dx, dy))
                    self.count += 1
                    self.maxy = max(self.maxy, maxy)

                dy += 1

            dx += 1

        return self.maxy, self.count


def main():
    target = load_input('data/day17/input.txt')
    print(target)

    solver = Solver(target)
    print(solver.solve())

    # trial = Trial(target, (7, -1))
    # print(trial.engage())


if __name__ == '__main__':
    main()


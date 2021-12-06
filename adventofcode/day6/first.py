from pathlib import Path

from rich import print


AVG_PERIOD = 7
INITIAL_PERIOD = 2


def load_input(filename: str) -> list[int]:
    lines = Path(filename).read_text().splitlines()
    numbers = lines[0].split(',')
    return [int(number) for number in numbers]


class FishSimulator:

    def __init__(self, days: int) -> None:
        self.mem = [0] * (days + 1)

    def fish(self, days: int) -> int:
        if self.mem[days]:
            return self.mem[days]

        if days > 9:
            next_cycle = self.fish(days - 7)
            children = self.fish(days - 9)
            self.mem[days] = next_cycle + children
            return self.mem[days]

        elif days > 7:
            next_cycle = self.fish(days - 7)
            self.mem[days] = 1 + next_cycle
            return self.mem[days]

        else:
            return 2

        # mem[2] = 1 + mem[1]
        # mem[3] = 1 + mem[1]

        # mem[14] = 1 + mem[7]
        # self.mem[7] = 2
        # self.mem[14] = 3
        # self.mem[21] = 4


class FishGame:

    def __init__(self, fishes: list[int], days: int) -> None:
        self.fishes = fishes
        self.day = 0
        self.days = days
        self.simulator = FishSimulator(days)

    def play(self) -> int:
        count = 0
        for fish in self.fishes:
            days = self.days - fish  # waits first reproduce period
            count += self.simulator.fish(days)

        return count

def main():
    fishes = load_input('data/day6/input.txt')
    game = FishGame(fishes, 256)
    print(game.play())


if __name__ == '__main__':
    main()

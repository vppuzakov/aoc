from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Optional, Tuple


BoardConfig = list[int, list[int]]

def rotate(a, b):
    pass


class Board:

    def __init__(self, config: BoardConfig) -> None:
        self.numbers = {}
        self.rows = [set() for i in range(5)]
        self.cols = [set() for i in range(5)]

        for i in range(5):
            for j in range(5):
                self.rows[i].add(config[i][j])
                self.cols[j].add(config[i][j])
                self.numbers[config[i][j]] = (i, j)

    def play(self, number: int) -> bool:
        if number not in self.numbers:
            return False

        i, j = self.numbers.pop(number)
        row = self.rows[i]
        col = self.cols[j]
        row.remove(number)
        col.remove(number)

        return not bool(row) or not bool(col)

    def __repr__(self) -> str:
        return f'all: {len(self.numbers)} rows: {self.rows} cols: {self.cols}'


@dataclass
class GameConfig:
    numbers: list[int]
    boards: list[BoardConfig]

    def __repr__(self) -> str:
        return f'Game: {self.numbers} board: {len(self.boards)}'


class Game:

    def __init__(self, game: GameConfig) -> None:
        self.numbers = game.numbers
        self.position = 0
        self.boards = [Board(board) for board in game.boards]

    @property
    def number(self) -> int:
        return self.numbers[self.position]

    def play(self) -> Optional[Board]:
        number = self.numbers[self.position]

        for board in self.boards:
            if board.play(number):
                print(f'winning board found: {number}')
                return board

        self.position += 1
        return None

    def find_winner(self) -> Board:
        winner = None
        while not winner:
            print(f'play number: {self.position}')
            winner = self.play()

        return winner

    def find_looser(self) -> Board:
        self.position = 0
        while self.boards:
            # print(f'play number: {self.position}')
            winner = self.find_winner()
            self.boards.remove(winner)

        return winner


def generate_board(lines: list[str]) -> BoardConfig:
    board = []
    for line in lines:
        row = line.split()
        board.append([int(number) for number in row])

    return board


def load_input(filename: str) -> GameConfig:
    lines = Path(filename).read_text().splitlines()
    numbers = [int(number) for number in lines[0].split(',')]
    boards_count = (len(lines) - 2) // 6
    lines = lines[2:]
    boards = []
    for board in range(boards_count):
        print(board)
        print(lines[board * 6:board * 6 + 5])
        boards.append(generate_board(lines[board * 6:board * 6 + 5]))

    return GameConfig(numbers=numbers, boards=boards)


def main():
    config = load_input('data/day4/input.txt')
    game = Game(config)
    winner = game.find_looser()
    print(winner.numbers.keys())
    unselected_sum = reduce(lambda acc, value: acc + value, winner.numbers.keys())
    result = unselected_sum * game.number

    print(f'last number: {game.number}')
    print(f'result: {result}')


if __name__ == '__main__':
    main()

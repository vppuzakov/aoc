from pathlib import Path
from typing import Optional

from rich import print


def load_input(filename: str) -> list[str]:
    lines = Path(filename).read_text().splitlines()
    return lines


class Solver:

    closing = {
        '}': '{',
        ')': '(',
        '>': '<',
        ']': '[',
    }

    scorer = {
        '}': 1197,
        ')': 3,
        '>': 25137,
        ']': 57,
    }

    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def solve(self) -> int:
        score = 0
        for line in self.lines:
            corruption = self.get_curruption(line)
            if corruption is not None:
                score += self.scorer[line[corruption]]

        return score

    def get_curruption(self, line: str) -> Optional[int]:
        mem = []
        for idx, ch in enumerate(line):
            if ch not in self.closing:
                mem.append(ch)
                continue

            expected_pair = self.closing[ch]
            if not mem:
                return idx

            open_pair = mem.pop()
            if open_pair != expected_pair:
                return idx

        return None


def main():
    lines = load_input('data/day10/input.txt')
    print(lines)
    solver = Solver(lines)
    print(solver.solve())


if __name__ == '__main__':
    main()

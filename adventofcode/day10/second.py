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

    opening = {
        '{': '}',
        '(': ')',
        '<': '>',
        '[': ']',
    }

    scorer = {
        '}': 3,
        ')': 1,
        '>': 4,
        ']': 2,
    }

    def __init__(self, lines: list[str]) -> None:
        self.lines = lines

    def solve(self) -> int:
        total = []
        for line in self.lines:
            score = 0
            corrupted, mem, _ = self.get_curruption(line)
            if corrupted:
                continue

            for ch in reversed(mem):
                closing_pair = self.opening[ch]
                score *= 5
                score += self.scorer[closing_pair]

            total.append(score)

        return sorted(total)[len(total) // 2]

    def get_curruption(self, line: str) -> tuple[bool, list[str], int]:
        mem = []
        for idx, ch in enumerate(line):
            if ch not in self.closing:
                mem.append(ch)
                continue

            expected_pair = self.closing[ch]
            if not mem:
                return True, [], idx

            open_pair = mem.pop()
            if open_pair != expected_pair:
                return True, [], idx

        return False, mem, -1


def main():
    lines = load_input('data/day10/input.txt')
    print(lines)
    solver = Solver(lines)
    print(solver.solve())


if __name__ == '__main__':
    main()

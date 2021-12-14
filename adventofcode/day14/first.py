from collections import Counter
from dataclasses import dataclass
from functools import total_ordering
from pathlib import Path

from rich import print


@dataclass
class Rule:
    src: str
    dst: str


def load_input(filename: str) -> tuple[str, list[Rule]]:
    lines = Path(filename).read_text().split('\n\n')
    template = lines[0]
    rules = [line for line in lines[1].split('\n') if line]
    rule_parts = [rule.split('->') for rule in rules]
    return template, [Rule(src.strip(), dst.strip()) for src, dst in rule_parts]


class Solver:

    def __init__(self, template: str, rules: list[Rule]) -> None:
        self.template = [code for code in template]
        self.rules = {rule.src: rule.dst for rule in rules}
        self.mem = {}

    def solve(self, steps: int) -> int:
        total = Counter(self.template)

        for i in range(1, len(self.template)):
            pair = ''.join(self.template[i-1:i+1])
            counter = self.find(pair, steps)
            total.update(counter)

        result = total.most_common()
        print(result[0], result[-1])
        return result[0][1] - result[-1][1]

    def find(self, pair: str, steps: int) -> list[str]:
        result = self.mem.get((pair, steps))
        if result:
            return result

        insertion = self.rules.get(pair)
        if not insertion:
            return {}

        if steps == 1:
            return {insertion: 1}

        counter = Counter({insertion: 1})
        left = self.find(f'{pair[0]}{insertion}', steps - 1)
        right = self.find(f'{insertion}{pair[1]}', steps - 1)
        counter.update(left)
        counter.update(right)

        self.mem[(pair, steps)] = counter
        return counter


def main():
    template, rules = load_input('data/day14/input.txt')
    print(template, rules)
    solver = Solver(template, rules)
    print(solver.solve(40))


if __name__ == '__main__':
    main()

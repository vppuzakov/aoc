from collections import Counter
from dataclasses import dataclass
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
        self.template = template
        self.rules = {rule.src: rule.dst for rule in rules}

    def solve(self) -> int:
        for i in range(40):
            print(f'step: {i}')
            self.step()

        counter = Counter(self.template).most_common()
        print(counter[0], counter[-1])
        return counter[0][1] - counter[-1][1]

    def step(self) -> None:
        template = []
        for i in range(1, len(self.template)):
            template.append(self.template[i - 1])
            pair = f'{self.template[i - 1]}{self.template[i]}'
            insertion = self.rules.get(pair)
            if insertion:
                template.append(insertion)

        template.append(self.template[-1])
        self.template = ''.join(template)


def main():
    template, rules = load_input('data/day14/input.txt')
    print(template, rules)
    solver = Solver(template, rules)
    print(solver.solve())


if __name__ == '__main__':
    main()

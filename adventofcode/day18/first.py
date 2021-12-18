from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Optional

from rich import print


@dataclass
class SailfishPair:
    left: Optional['SailfishPair'] = None
    right: Optional['SailfishPair'] = None
    parent: Optional['SailfishPair'] = None
    val: Optional[int] = None

    @property
    def isleft(self) -> bool:
        return self.parent and self.parent.left == self

    @property
    def isright(self) -> bool:
        return self.parent and self.parent.right == self

    @property
    def isroot(self) -> bool:
        return self.parent is None

    @property
    def adjleft(self) -> Optional['SailfishPair']:
        upper = self.parent
        while upper:
            if upper.isright:
                return upper.left

            upper = upper.parent

        return None

    @property
    def adjright(self) -> Optional['SailfishPair']:
        upper = self.parent
        while upper:
            if upper.isleft:
                return upper.parent.right if self.isright else upper.right

            upper = upper.parent

        return None

    @property
    def adjacent(self) -> Optional['SailfishPair']:
        return self.adjright if self.isright else self.adjleft

    def __repr__(self) -> str:
        return f'[{self.left}, {self.right}]' if self.left and self.right else str(self.val)


def convert(line: str, parent: SailfishPair = None) -> SailfishPair:
    if len(line) == 1:
        return SailfishPair(val=int(line), parent=parent)

    count = 0
    for position, ch in enumerate(line):
        if ch == '[':
            count += 1

        if ch == ']':
            count -= 1

        if ch == ',' and count == 1:
            pair = SailfishPair(parent=parent)
            pair.left = convert(line[1:position], pair)
            pair.right = convert(line[position + 1:-1], pair)
            return pair


def load_input(filename: str) -> list[SailfishPair]:
    lines = Path(filename).read_text().splitlines()
    return [convert(line) for line in lines]


def find_explosion(pair: SailfishPair, level: int = 0) -> Optional[SailfishPair]:
    if not pair:
        return None

    if level == 5:
        return pair.parent

    explosion = find_explosion(pair.left, level + 1)
    if explosion:
        return explosion

    return find_explosion(pair.right, level + 1)


def explode(pair: SailfishPair) -> SailfishPair:
    adjleft = pair.adjleft
    if adjleft:
        adjleft.val += pair.left.val

    adjright = pair.adjright
    if adjright:
        adjright.val += pair.right.val

    if pair.isleft:
        pair.parent.left = SailfishPair(val=0)

    if pair.isright:
        pair.parent.right = SailfishPair(val=0)


def splits(pair: SailfishPair) -> SailfishPair:
    return pair


def reduce(pair: SailfishPair) -> SailfishPair:
    return pair


def add(left: SailfishPair, right: SailfishPair) -> SailfishPair:
    result = SailfishPair(left, right)
    return reduce(result)


class Solver:

    def __init__(self, pairs: list[SailfishPair]) -> None:
        self.pairs = pairs

    def solve(self) -> SailfishPair:
        result = self.pairs[0]
        for pair in self.pairs[1:]:
            result = add(result, pair)

        return result


def explosion(line: str) -> str:
    number = convert(line)
    explosion = find_explosion(number)
    print(explosion)
    explode(explosion)
    return number


def main():
    assert str(explosion('[[[[[9,8],1],2],3],4]')) == str(convert('[[[[0,9],2],3],4]'))
    assert str(explosion('[7,[6,[5,[4,[3,2]]]]]')) == str(convert('[7,[6,[5,[7,0]]]]'))
    assert str(explosion('[[6,[5,[4,[3,2]]]],1]')) == str(convert('[[6,[5,[7,0]]],3]'))

    return

    pairs = load_input('data/day18/dev.txt')
    for pair in pairs:
        print(pair)

    solver = Solver(pairs)
    print('\n\nresult:\n')
    print(solver.solve())


if __name__ == '__main__':
    main()

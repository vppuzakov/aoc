from copy import deepcopy
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
    def magnitude(self) -> None:
        if self.val is not None:
            return self.val

        return 3 * self.left.magnitude + 2 * self.right.magnitude

    @property
    def root(self) -> 'SailfishPair':
        current = self
        while current.parent:
            current = current.parent

        return current

    @property
    def isleft(self) -> bool:
        return self.parent is not None and self.parent.left is self

    @property
    def isright(self) -> bool:
        return self.parent is not None and self.parent.right is self

    @property
    def isroot(self) -> bool:
        return self.parent is None

    @property
    def rightmost(self) -> 'SailfishPair':
        pair = self
        while pair.right:
            pair = pair.right

        return pair

    @property
    def leftmost(self) -> 'SailfishPair':
        pair = self
        while pair.left:
            pair = pair.left

        return pair

    @property
    def adjleft(self) -> Optional['SailfishPair']:
        upper = self
        while upper and upper.isleft:
            upper = upper.parent

        return upper.parent.left.rightmost if upper is not self.root else None

    @property
    def adjright(self) -> Optional['SailfishPair']:
        upper = self

        while upper and upper.isright:
            upper = upper.parent

        return upper.parent.right.leftmost if upper is not self.root else None

    def __repr__(self) -> str:
        return f'[{self.left}, {self.right}]' if self.left and self.right else str(self.val)


def convert(line: str, parent: SailfishPair = None) -> SailfishPair:
    if ',' not in line:
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


def find_splits(pair: Optional[SailfishPair]) -> Optional[SailfishPair]:
    if not pair:
        return None

    if pair.val and pair.val >= 10:
        return pair

    splits = find_splits(pair.left)
    if splits:
        return splits

    return find_splits(pair.right)


def find_explosion(pair: Optional[SailfishPair], level: int = 0) -> Optional[SailfishPair]:
    if pair is None:
        return None

    if level == 5:
        return pair.parent

    if pair.val is not None:
        return None

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
        pair.parent.left = SailfishPair(val=0, parent=pair.parent)

    if pair.isright:
        pair.parent.right = SailfishPair(val=0, parent=pair.parent)


def split(pair: SailfishPair) -> None:
    half = pair.val // 2
    pair.left = SailfishPair(val=half, parent=pair)
    pair.right = SailfishPair(val=half + pair.val % 2, parent=pair)
    pair.val = None


def reduce(pair: SailfishPair) -> None:
    reduced = False

    while not reduced:
        # print(pair)
        explosion = find_explosion(pair)
        if explosion:
            explode(explosion)
            continue

        split_pair = find_splits(pair)
        if split_pair:
            split(split_pair)
            continue

        reduced = True


def explosion(line: str) -> str:
    number = convert(line)
    explosion = find_explosion(number)
    print(explosion)
    explode(explosion)
    print(number)
    return number


def reduction(line: str) -> str:
    number = convert(line)
    reduce(number)
    return str(number)


def traverse(pair: Optional[SailfishPair]) -> Generator[SailfishPair, SailfishPair, None]:
    if not pair:
        return

    yield pair

    yield from traverse(pair.left)
    yield from traverse(pair.right)


def add(first: SailfishPair, second: SailfishPair) -> SailfishPair:
    first = deepcopy(first)
    second = deepcopy(second)
    pair = SailfishPair(first, second)
    first.parent = pair
    second.parent = pair
    reduce(pair)
    return pair


class Solver:

    def __init__(self, pairs: list[SailfishPair]) -> None:
        self.pairs = pairs

    def solve(self) -> SailfishPair:
        result = self.pairs[0]
        for pair in self.pairs[1:]:
            result = add(result, pair)

        return result

    def largest_sum(self) -> int:
        largest = -1
        for first in self.pairs:
            for second in self.pairs:
                if first is second:
                    continue

                result = add(first, second)
                largest = max(result.magnitude, largest)

        return largest

def main():
    # assert str(explosion('[[[[[9,8],1],2],3],4]')) == str(convert('[[[[0,9],2],3],4]'))
    # assert str(explosion('[7,[6,[5,[4,[3,2]]]]]')) == str(convert('[7,[6,[5,[7,0]]]]'))
    # assert str(explosion('[[6,[5,[4,[3,2]]]],1]')) == str(convert('[[6,[5,[7,0]]],3]'))
    # assert str(explosion('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]')) == str(convert('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'))
    # assert str(explosion('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')) == str(convert('[[3,[2,[8,0]]],[9,[5,[7,0]]]]'))
    # assert str(explosion('[[[[0,7],4],[7,[[8,4],9]]],[1,1]]')) == str(convert('[[[[0,7],4],[15,[0,13]]],[1,1]]'))

    # assert reduction('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]') == str(convert('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'))
    # assert reduction('[[[[[1,1],[2,2]],[3,3]],[4,4]],[5,5]]') == str(convert('[[[[3,0],[5,3]],[4,4]],[5,5]]'))
    # assert reduction('[[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]')

    pairs = load_input('data/day18/input.txt')

    solver = Solver(pairs)
    result = solver.solve()
    print('\n\nresult:\n')
    print(result)
    print(f'{result.magnitude=}')
    print(f'{solver.largest_sum()}')


if __name__ == '__main__':
    main()

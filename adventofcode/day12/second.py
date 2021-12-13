from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from rich import print


@dataclass
class Cave:
    name: str
    connections: list['Cave'] = field(default_factory=list)

    @property
    def is_big(self) -> bool:
        return self.name.isupper()

    @property
    def max_visits(self) -> int:
        return 2 if self.name != 'start' and self.name != 'end' else 1

    def __repr__(self) -> str:
        return f'Cave({self.name} -> {[cave.name for cave in self.connections]})'


@dataclass
class Connection:
    first: str
    second: str

    def __repr__(self) -> str:
        return f'{self.first}-{self.second}'


def load_input(filename: str) -> list[Connection]:
    lines = Path(filename).read_text().splitlines()
    connections = [line.split('-') for line in lines]
    return [Connection(first, second) for first, second in connections]


class Solver:

    def __init__(self, connections: list[Connection]) -> None:
        self.connections = connections
        self.caves = self.load_caves()

    def load_caves(self) -> dict[str, Cave]:
        caves = {}
        for connection in self.connections:
            first = caves.get(connection.first) or Cave(connection.first)
            caves[connection.first] = first

            second = caves.get(connection.second) or Cave(connection.second)
            caves[connection.second] = second

            first.connections.append(second)
            second.connections.append(first)

        return caves

    def solve(self) -> int:
        print(self.caves)
        count = 0
        for _, found, path in self.traverse(self.caves['start']):
            if not found:
                continue

            # print(found, path)

            count += 1

        return count

    def traverse(
        self,
        cave: Cave,
        source: Cave = None,
        visited_nodes: dict[str, int] = None,
        visited_path: set[tuple[str, str]] = None,
        path: list[str] = None,
        twice_visits_allowed: bool = True,
    ) -> Cave:
        visited_nodes = visited_nodes or defaultdict(int)
        visited_path = visited_path or set()
        path = path or []

        if cave.name == 'end':
            path.append(cave.name)
            yield cave, True, ','.join(path)
            return

        visits = visited_nodes[cave.name]

        max_visits = cave.max_visits if twice_visits_allowed else 1
        if not cave.is_big and visits >= max_visits:
            yield cave, False, ','.join(path)
            return

        if visits == 1 and not cave.is_big and cave.name != 'start' and twice_visits_allowed:
            twice_visits_allowed = False

        visited_nodes = visited_nodes.copy()
        visited_nodes[cave.name] += 1

        path = path.copy()
        path.append(cave.name)

        yield cave, False, ','.join(path)

        for connected in cave.connections:
            yield from self.traverse(connected, cave, visited_nodes, visited_path, path, twice_visits_allowed)


def main():
    connections = load_input('data/day12/input.txt')
    print(connections)
    solver = Solver(connections)
    print(solver.solve())


if __name__ == '__main__':
    main()

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
        for _, found, _ in self.traverse(self.caves['start']):
            if not found:
                continue

            count += 1

        return count

    def traverse(
        self,
        cave: Cave,
        source: Cave = None,
        visited_nodes: set[str] = None,
        visited_path: set[tuple[str, str]] = None,
        path: list[str] = None,
    ) -> Cave:
        visited_nodes = visited_nodes or set()
        visited_path = visited_path or set()
        path = path or []

        if source and (source.name, cave.name) in visited_path:
            yield cave, False, ','.join(path)
            return

        if cave.name == 'end':
            path.append(cave.name)
            yield cave, True, ','.join(path)
            return

        if not cave.is_big and cave.name in visited_nodes:
            yield cave, False, ','.join(path)
            return

        visited_nodes = visited_nodes.copy()
        visited_nodes.add(cave.name)

        path = path.copy()
        path.append(cave.name)

        if source:
            visited_path = visited_path.copy()
            visited_path.add((source.name, cave.name))

        yield cave, False, ''.join(path)

        for connected in cave.connections:
            yield from self.traverse(connected, cave, visited_nodes, visited_path, path)


def main():
    connections = load_input('data/day12/input.txt')
    print(connections)
    solver = Solver(connections)
    print(solver.solve())


if __name__ == '__main__':
    main()

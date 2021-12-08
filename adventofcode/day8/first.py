from dataclasses import dataclass
from pathlib import Path

from rich import print


@dataclass
class Entry:
    signal: list[str]
    output: list[str]

    def __repr__(self) -> str:
        return f'{self.signal} | {self.output}'


def load_input(filename: str) -> list[Entry]:
    lines = Path(filename).read_text().splitlines()
    entries = (row.split('|') for row in lines if row)
    return [
        Entry(signal.split(), output.split())
        for signal, output in entries
    ]


class EntryParser:

    len_to_digits = {
        2: 1,
        3: 7,
        4: 4,
        7: 8,
    }

    codes = 'abcdefg'

    def __init__(self, entry: Entry) -> None:
        self.entry = entry
        self.decode_map = {code: set(self.codes) for code in self.codes}

    def count_unique_digits_output(self) -> int:
        counter = 0
        for digit in self.entry.output:
            if len(digit) in self.len_to_digits:
                counter += 1

        return counter

    def decode(self) -> int:
        pass


def main():
    entries = load_input('data/day8/mini.txt')
    counter = 0
    for entry in entries:
        parser = EntryParser(entry)
        counter += parser.count_unique_digits_output()

    print(counter)


if __name__ == '__main__':
    main()

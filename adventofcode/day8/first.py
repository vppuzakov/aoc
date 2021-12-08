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

    digits = {
        0: 'abcefg',
        1: 'cf',
        2: 'acdeg',
        3: 'acdfg',
        4: 'bcdf',
        5: 'abdfg',
        6: 'abdefg',
        7: 'acf',
        8: 'abcdefg',
        9: 'abcdfg',
    }

    codes = 'abcdefg'

    def __init__(self, entry: Entry) -> None:
        self.entry = entry
        self.map = {}

    def count_unique_digits_output(self) -> int:
        counter = 0
        for digit in self.entry.output:
            if len(digit) in self.len_to_digits:
                counter += 1

        return counter

    def create_decode_map(self) -> None:
        for digit in self.entry.signal:
            print(digit)
            decoded_digit = self.len_to_digits.get(len(digit))
            if decoded_digit:
                self.map[decoded_digit] = digit

        self.map[3] = self.find_3()
        self.map[5] = self.find_5()
        self.map[2] = self.find_2()
        self.map[0] = self.find_0()
        self.map[9] = self.find_9()
        self.map[6] = self.find_6()

        print(self.map)

    def find_9(self) -> None:
        sixes = [digit for digit in self.entry.signal if len(digit) == 6 and digit != self.map[0]]
        for digit in sixes:
            if set(digit) & set(self.map[7]) == set(self.map[7]):
                return digit

    def find_6(self) -> None:
        sixes = [digit for digit in self.entry.signal if len(digit) == 6 and digit != self.map[0] and digit != self.map[9]]
        return sixes[0]

    def find_0(self) -> None:
        sixes = [digit for digit in self.entry.signal if len(digit) == 6]
        for digit in sixes:
            if len(set(digit) - set(self.map[5])) == 2:
                return digit

    def find_3(self) -> None:
        fives = [digit for digit in self.entry.signal if len(digit) == 5]
        for digit in fives:
            if len(set(digit) - set(self.map[7])) == 2:
                return digit

    def find_5(self) -> None:
        fives = [digit for digit in self.entry.signal if len(digit) == 5 and digit != self.map[3]]
        for digit in fives:
            if len(set(digit) - set(self.map[4])) == 2:
                return digit

    def find_2(self) -> None:
        fives = [digit for digit in self.entry.signal if len(digit) == 5 and digit != self.map[3] and digit != self.map[5]]
        return fives[0]

    def decode_output_digit(self, output_digit: str) -> str:
        for digit, code in self.map.items():
            if set(code) == set(output_digit):
                return str(digit)

        return None

    def decode(self) -> int:
        self.create_decode_map()
        number = ''.join(self.decode_output_digit(digit) for digit in self.entry.output)
        return int(number)


def main():
    entries = load_input('data/day8/input.txt')
    counter = 0
    for entry in entries:
        parser = EntryParser(entry)
        counter += parser.decode()

    print(counter)


if __name__ == '__main__':
    main()

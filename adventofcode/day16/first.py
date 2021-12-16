from os import remove
from pathlib import Path

from rich import print


def load_input(filename: str) -> str:
    lines = Path(filename).read_text().splitlines()
    return lines[0]


class LiteralPacket:

    def __init__(self, code: str) -> None:
        self.code = code

    def decode(self) -> int:
        code = self.code
        print(f'literal code: {code}')

        code = self.skip_leading_zeros(code)
        print(f'skip leading zeros: {code}')

        groups = self.split_groups(code)
        groups = list(self.remove_prefix_groups(groups))

        return int(''.join(groups), 2)

    def skip_leading_zeros(self, code: str) -> str:
        i, skip_count = 0, 0
        while i < len(code) and code[i] == 0:
            skip_count += 1
            i += 1

        return code[skip_count:]

    def split_groups(self, code: str) -> list[str]:
        groups = []
        i = 0

        while i < len(code):
            groups.append(code[i:i + 5])
            if code[i] == '0':
                break

            i += 5

        return groups

    def remove_prefix_groups(self, groups: list[str]) -> list[str]:
        return [group[1:] for group in groups]


class Transmission:

    def __init__(self, transmission: str) -> None:
        self.transmission = transmission
        self.binarycode = self.to_bits()
        self.version = self.get_version()
        self.typeid = self.get_typeid()

    def to_bits(self) -> list[str]:
        codes = [f'{int(ch, 16):04b}' for ch in self.transmission]
        binarycode = ''.join(codes)
        return binarycode

    def get_version(self) -> int:
        return int(''.join(self.binarycode[:3]), 2)

    def get_typeid(self) -> int:
        return int(''.join(self.binarycode[3:6]), 2)

    def decode(self) -> str:
        print(f'{self.binarycode=}')
        print(f'{self.version=} {self.typeid=}')

        if self.typeid == 4:
            packet = LiteralPacket(self.binarycode[6:])
            return packet.decode()


def main():
    lines = load_input('data/day16/dev.txt')
    print(lines)
    transmission = Transmission(lines)
    print(transmission.decode())


if __name__ == '__main__':
    main()

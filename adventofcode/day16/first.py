from abc import ABC
from os import remove
from pathlib import Path

from rich import print


def load_input(filename: str) -> str:
    lines = Path(filename).read_text().splitlines()
    return lines[0]


class Packet(ABC):

    def __init__(self, code: str, version: int, typeid: int) -> None:
        self.code = code
        self.version = version
        self.typeid = typeid
        self.tail: str = ...

    def total_versions(self) -> int:
        ...


def get_version(code: str) -> int:
    return int(''.join(code[:3]), 2)


def get_typeid(code: str) -> int:
    return int(''.join(code[3:6]), 2)


def create_packet(code: str) -> tuple[Packet, str]:
    version = get_version(code)
    typeid = get_typeid(code)
    body = code[6:]

    if typeid == 4:
        packet = LiteralPacket(body, version, typeid)
        return packet, packet.tail

    packet = OperatorPacket(body, version, typeid)
    return packet, packet.tail


class OperatorPacket(Packet):

    def __init__(self, code: str, version: int, typeid: int) -> None:
        super().__init__(code, version, typeid)
        self.subpackets, self.tail = self.get_subpackets(code)

    def get_subpackets(self, code: str) -> tuple[list[Packet], str]:
        length_type_id = self.code[0]
        if length_type_id == '0':
            packets_bits_count = int(self.code[1:16], 2)
            print(f'{packets_bits_count=}')
            return self.parse_subpacket_bits(packets_bits_count, self.code[16:])
        else:
            packets_count = int(self.code[1:12], 2)
            print(f'{packets_count=}')
            return self.parse_subpackets_len(packets_count, self.code[12:])

    def parse_subpacket_bits(self, count: int, code: str) -> tuple[list[Packet], str]:
        tail = code[count:] if count < len(code) else ''
        code = code[:count]
        packets = []
        while code:
            packet, code = create_packet(code)
            packets.append(packet)

        return packets, tail

    def parse_subpackets_len(self, count: int, code: str) -> tuple[list[Packet], str]:
        packets = []
        for _ in range(count):
            packet, code = create_packet(code)
            packets.append(packet)

        return packets, code

    def __repr__(self) -> str:
        return f'{self.subpackets=} {self.tail=}'

    def total_versions(self) -> int:
        total = self.version
        for packet in self.subpackets:
            total += packet.total_versions()

        return total


class LiteralPacket(Packet):

    def __init__(self, code: str, version: int, typeid: int) -> None:
        super().__init__(code, version, typeid)
        self.val, self.tail = self.decode()

    def decode(self) -> tuple[int, str]:
        code = self.code
        print(f'literal code: {code}')

        code = self.skip_leading_zeros(code)
        print(f'skip leading zeros: {code}')

        groups, tail = self.split_groups(code)
        groups = list(self.remove_prefix_groups(groups))

        return int(''.join(groups), 2), tail

    def skip_leading_zeros(self, code: str) -> str:
        i, skip_count = 0, 0
        while i < len(code) and code[i] == 0:
            skip_count += 1
            i += 1

        return code[skip_count:]

    def split_groups(self, code: str) -> tuple[list[str], str]:
        groups = []
        i = 0

        while i < len(code):
            groups.append(code[i:i + 5])
            if code[i] == '0':
                break

            i += 5

        return groups, code[i + 5:]

    def remove_prefix_groups(self, groups: list[str]) -> list[str]:
        return [group[1:] for group in groups]

    def __repr__(self) -> str:
        return str(self.val)

    def total_versions(self) -> int:
        return self.version


class Transmission:

    def __init__(self, transmission: str) -> None:
        self.packet, self.tail = self.decode(transmission)

    def to_bits(self, transmission: str) -> list[str]:
        codes = [f'{int(ch, 16):04b}' for ch in transmission]
        return ''.join(codes)

    def decode(self, transmission: str) -> Packet:
        code = self.to_bits(transmission)
        print(f'{code=}')
        return create_packet(code)

    def total_versions(self) -> int:
        return self.packet.total_versions()


def main():
    data = load_input('data/day16/input.txt')
    print(data)

    transmission = Transmission(data)
    print(transmission.packet)
    print(transmission.tail)

    print(f'{transmission.total_versions()=}')


if __name__ == '__main__':
    main()

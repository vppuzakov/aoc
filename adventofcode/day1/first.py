from pathlib import Path

def load_depths(filename: str):
    lines = Path(filename).read_text().splitlines()
    return [int(line) for line in lines]


def count_increases(depths: list[int]) -> int:
    increases = 0
    for i in range(len(depths) - 1):
        if depths[i + 1] > depths[i]:
            increases += 1

    return increases


def main():
    depths = load_depths('data/day1/input1.txt')
    increases = count_increases(depths)
    print(increases)


if __name__ == '__main__':
    main()

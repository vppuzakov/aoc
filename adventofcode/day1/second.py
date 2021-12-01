from pathlib import Path

def load_depths(filename: str):
    lines = Path(filename).read_text().splitlines()
    return [int(line) for line in lines]


def count_increases(depths: list[int]) -> int:
    increases = 0
    prev = -1
    for i in range(len(depths) - 3):
        window = sum(depths[i:i+3])
        print(prev, window)
        if window > prev:
            increases += 1

        prev = window

    return increases


def main():
    depths = load_depths('data/day1/input1.txt')
    increases = count_increases(depths)
    print(increases)


if __name__ == '__main__':
    main()

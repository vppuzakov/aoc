from pathlib import Path

def load_report(filename: str) -> list[str]:
    return Path(filename).read_text().splitlines()


def get_power(report: list[str]) -> int:
    size = len(report[0])
    gamma, epsilon = [], []
    for i in range(size):
        counter = {'0': 0, '1': 0}
        for row in report:
            counter[row[i]] += 1

        gamma.append('1' if counter['1'] > counter['0'] else '0')
        epsilon.append('1' if counter['1'] < counter['0'] else '0')

    return int(''.join(gamma), 2) * int(''.join(epsilon), 2)


def main():
    report = load_report('data/day3/input1.txt')
    power = get_power(report)
    print(power)


if __name__ == '__main__':
    main()

from pathlib import Path


def load_report(filename: str) -> list[str]:
    return Path(filename).read_text().splitlines()


def get_criteria_number(report: list[str], idx, criteria) -> str:
    counter = {'0': 0, '1': 0}
    for row in report:
        counter[row[idx]] += 1

    return '1' if criteria(counter['1'], counter['0']) else '0'


def filter_rows(report: list[str], criteria) -> int:
    size = len(report[0])
    result = report.copy()

    for i in range(size):
        number = get_criteria_number(result, i, criteria)
        result = list(filter(lambda row: row[i] == number, result))
        if len(result) == 1:
            return int(result[0], 2)


def get_rating(report) -> int:
    oxygen = filter_rows(report, lambda a, b: a >= b)
    carbon = filter_rows(report, lambda a, b: a < b)
    return oxygen * carbon


def main():
    report = load_report('data/day3/input1.txt')
    rating = get_rating(report)
    print(rating)


if __name__ == '__main__':
    main()

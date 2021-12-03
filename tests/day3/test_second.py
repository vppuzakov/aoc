import pytest

from adventofcode.day3.second import get_rating


@pytest.fixture
def report():
    return [
        '00100',
        '11110',
        '10110',
        '10111',
        '10101',
        '01111',
        '00111',
        '11100',
        '10000',
        '11001',
        '00010',
        '01010',
    ]


def test_power(report):
    assert get_rating(report) == 230

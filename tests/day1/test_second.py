import pytest

from adventofcode.day1.second import count_increases


@pytest.fixture
def depths():
    return [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_increases(depths):
    increases = count_increases(depths)
    assert increases == 5

from re import sub

import pytest

from adventofcode.day2.second import Directions, Movement, move


@pytest.fixture
def courses():
    return [
        Movement(Directions.FORWARD, 5),
        Movement(Directions.DOWN, 5),
        Movement(Directions.FORWARD, 8),
        Movement(Directions.UP, 3),
        Movement(Directions.DOWN, 8),
        Movement(Directions.FORWARD, 2),
    ]

def test_move(courses):
    submarine = move(courses)
    assert submarine.position == 15
    assert submarine.depth == 60
    assert submarine.position * submarine.depth == 900

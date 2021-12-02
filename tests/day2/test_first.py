from re import sub

import pytest

from adventofcode.day2.first import Directions, Movement, move


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
    assert submarine.position * submarine.depth == 150

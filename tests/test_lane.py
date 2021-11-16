from src.lane import Lane
from src.exceptions import *

import pytest
import numpy as np


def test_push():
    lane = Lane(20, p_slow=0, green=False)
    lane.push([5, 10])
    assert list(lane.positions) == [5, 10]
    assert list(lane.speeds) == [0, 0]

    lane.push([6], [2])
    assert list(lane.positions) == [4, 5, 10]
    assert list(lane.speeds) == [2, 0, 0]

    lane.push([])
    assert list(lane.positions) == [4, 5, 10]

    lane.push([8, 9])
    assert list(lane.positions) == [2, 3, 4, 5, 10]


def test_push_errors():
    lane = Lane(3)
    with pytest.raises(TooCrowded):
        lane.push([1, 2, 3, 4])

    lane = Lane(10)
    lane.push([2])
    with pytest.raises(TooCrowded):
        lane.push([1, 2, 3])

    lane = Lane(10)
    with pytest.raises(ValueError):
        lane.push([1, 2], [0])


def test_flush():
    lane = Lane(10)
    lane.positions = np.array([5, 10, 15])
    lane.flush()
    assert list(lane.positions) == [5]

    lane = Lane(0)
    lane.flush()
    assert list(lane.positions) == []

    lane = Lane(10)
    lane.flush()
    assert list(lane.positions) == []


def test_closest_car():
    lane = Lane(10)
    assert lane.n_spaces_available() == 10
    lane.push([3, 6])
    assert lane.n_spaces_available() == 3


def test_statistics():
    lane = Lane(10)
    assert lane.n_queued() == 0
    assert lane.density() == 0
    assert lane.average_speed() == 0
    assert lane.flow() == 0

    lane.push([4, 5, 7, 8, 9])
    assert lane.density() == 0.5
    assert lane.n_queued() == 3
    assert lane.average_speed() == 0
    assert lane.flow() == 0

    lane = Lane(5)
    lane.positions = np.array([1, 2, 3])
    lane.speeds = np.array([0, 1, 2])
    assert lane.n_queued() == 0
    assert lane.average_speed() == 1
    assert lane.density() == 0.6
    assert lane.flow() == 0.6


def test_step():
    lane = Lane(10, p_slow=0)
    pos = np.array([3, 5, 9])
    lane.push(pos)
    lane.step()
    assert list(lane.positions) == [4, 6]

    lane = Lane(100, speed_limit=5, p_slow=0)
    lane.push([1, 20, 30], [10, 11, 12])
    lane.step()
    assert list(lane.speeds) == [5, 5, 5]

    lane = Lane(10, green=False)
    lane.push([1, 2, 3])
    for _ in range(25):
        lane.step()
    assert list(lane.positions) == [7, 8, 9]
    assert list(lane.speeds) == [0, 0, 0]


def test_to_array():
    lane = Lane(5, p_slow=0)
    lane.push(np.array([1, 2]))
    arr = [0, 1, 1, 0, 0]
    assert list(lane.to_array()) == arr

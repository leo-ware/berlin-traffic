from src.lane import Lane
from src.traffic_light import *
import pytest


def test_index_green():
    lanes = [Lane(10, green=True) for _ in range(10)]
    light = PeriodicAlternatingTrafficLight("foo", in_lanes=lanes)

    for lane in lanes:
        assert not lane.green
    assert light.index_green is None

    light.index_green = 5
    assert lanes[5].green
    light.index_green = 6
    assert not lanes[5].green
    assert lanes[6].green


def test_periodic():

    class TF(AbstractTrafficLight):
        counter = 0

        def n_step(self):
            self.__class__.counter += 1

    foo = TF("foo", period=10)
    for _ in range(100):
        foo.step()

    assert TF.counter == 10
    with pytest.raises(ValueError):
        TF("bar", period=0)


def test_periodic_alternating():
    light = PeriodicAlternatingTrafficLight(period=1, in_lanes=[Lane(), Lane(), Lane()])
    green_indices = []
    for step in range(5):
        light.step()
        green_indices.append(light.index_green)
    assert green_indices == [0, 1, 2, 0, 1]


def test_periodic_random():
    light = PeriodicRandomTrafficLight(period=1, in_lanes=[Lane(), Lane(), Lane()])
    green_indices = []
    for step in range(5):
        light.step()
        green_indices.append(light.index_green)
    assert sum(green_indices) <= 10


def test_periodic_adaptive():
    lane1 = Lane(5)
    lane2 = Lane(5)
    light = PeriodicRandomTrafficLight(period=1, in_lanes=[lane1, lane2])

    lane1.push([4])
    light.step()
    print(lane1.n_queued(), lane2.n_queued())
    assert light.index_green == 0

    lane2.push([3, 4])
    light.step()
    print(lane1.n_queued(), lane2.n_queued())
    assert light.index_green == 1

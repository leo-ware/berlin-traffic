from src.streets.lane import Lane
from src.intersections.traffic_light import PeriodicTrafficLight, AbstractTrafficLight
import pytest


def test_index_green():
    lanes = [Lane(10, green=True) for _ in range(10)]
    light = PeriodicTrafficLight(in_lanes=lanes)

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

    foo = TF(period=10)
    for _ in range(100):
        foo.step()

    assert TF.counter == 10
    with pytest.raises(ValueError):
        TF(period=0)

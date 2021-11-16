import pytest

from src.exceptions import NoOutlet, OneWayError
from src.on_ramp import OnRamp
from src.parking_lot import ParkingLot


def test_errs():
    ramp = OnRamp()
    with pytest.raises(NoOutlet):
        ramp.step()
    with pytest.raises(OneWayError):
        ramp.push([0])


def test_blocks():
    dead_end = OnRamp()
    ramp = OnRamp(next=dead_end)
    for _ in range(10):
        ramp.step()
    assert ramp.blocks == 10


def test_1():
    lot = ParkingLot()
    ramp = OnRamp(p=0, next=lot)
    for _ in range(10):
        ramp.step()
    assert lot.n_parked_cars == 0


def test_2():
    lot = ParkingLot()
    ramp = OnRamp(p=1, next=lot)
    for _ in range(10):
        ramp.step()
    assert lot.n_parked_cars == 10

import pytest

from src.exceptions import NoOutlet, OneWayError
from src.on_ramp import OnRamp
from src.parking_lot import ParkingLot


def test_it():
    ramp = OnRamp()
    with pytest.raises(NoOutlet):
        ramp.step()

    lot = ParkingLot()
    ramp = OnRamp(p=0, next=lot)
    for _ in range(10):
        ramp.step()
    assert lot.n_parked_cars == 0

    lot = ParkingLot()
    ramp = OnRamp(p=1, next=lot)
    for _ in range(10):
        ramp.step()
    assert lot.n_parked_cars == 10

    with pytest.raises(OneWayError):
        ramp.push([0])

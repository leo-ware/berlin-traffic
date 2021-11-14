from src.parking_lot import ParkingLot
from src.on_ramp import OnRamp
from src.clover_leaf import CloverLeaf
from src.lane import Lane


def test_handoffs():
    # configuration 1
    lot = ParkingLot()
    ramp = OnRamp(next=lot)
    for _ in range(10):
        ramp.step()
    assert lot.n_parked_cars == 10

    # configuration 2
    lot = ParkingLot()
    leaf = CloverLeaf(out_lanes=[lot])
    ramp = OnRamp(next=leaf)
    for _ in range(10):
        ramp.step()
    assert lot.n_parked_cars == 10

    # configuration 3
    lot = ParkingLot()
    lane = Lane(length=20, next=lot, p_slow=0)
    leaf = CloverLeaf(out_lanes=[lane])
    ramp = OnRamp(next=leaf)

    for _ in range(10):
        ramp.step()
        lane.step()
        lane.step()

    for _ in range(100):
        lane.step()

    assert lot.n_parked_cars == 10

from src.parking_lot import ParkingLot
from src.on_ramp import OnRamp
from src.clover_leaf import CloverLeaf
from src.lane import Lane


def test_1():
    lot = ParkingLot()
    ramp = OnRamp(next=lot)
    for _ in range(10):
        ramp.step()
    assert lot.n_parked_cars == 10


def test_2():
    lot = ParkingLot()
    leaf = CloverLeaf(out_lanes=[lot])
    ramp = OnRamp(next=leaf)
    for _ in range(10):
        ramp.step()
    assert (lot.n_parked_cars + ramp.blocks) == 10


def test_3():
    lot = ParkingLot()
    lane = Lane(length=20, next=lot)
    leaf = CloverLeaf(out_lanes=[lane])
    ramp = OnRamp(next=leaf)

    leaf.setup()

    for _ in range(10):
        print("bro")
        print(ramp.next, ramp.next.space_available())
        lane = ramp.next.assignments.peak()
        print(lane, lane.space_available(), lane.n_spaces_available())
        ramp.step()
        lane.step()

    for _ in range(100):
        lane.step()

    assert (lot.n_parked_cars + ramp.blocks) == 10

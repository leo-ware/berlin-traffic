from src.network import build_network, Network
from src.clover_leaf import CloverLeaf
from src.graphs.simple import *


def test_init():
    n = Network()
    assert n.intersections == []
    assert n.lanes == []
    assert n.on_ramps == []
    assert n.parking_lots == []


def test_two_intersections():
    n = Network()
    a = CloverLeaf()
    b = CloverLeaf()

    n.connect(a, b, 10)
    assert set(n.intersections) == {a, b}
    assert len(n.lanes) == 2
    assert n.parking_lots == []

    l1, l2 = n.lanes

    b.setup()
    n.step()
    assert len(b.out_lanes) == 1
    assert l1.n_cars() == l2.n_cars() == 0

    n.add_entry(b)
    assert len(n.on_ramps) == 1
    ramp = n.on_ramps[0]

    n.step()
    assert l1.n_cars() + l2.n_cars() == 1
    n.step()
    assert l1.n_cars() + l2.n_cars() + ramp.blocks == 2


def test_running():
    n = Network()
    a = CloverLeaf()
    b = CloverLeaf()

    n.connect(a, b, 10)
    n.add_entry(a)
    n.add_exit(b)

    # make sure we got connected right
    assert len(a.out_lanes) == 1
    assert len(b.out_lanes) == 2
    assert len(a.in_lanes) == 1
    assert len(b.in_lanes) == 1
    assert {lane.next for *_, lane in n.graph.edges.data("lane") if lane} == {a, b}

    assert len(n.parking_lots) == 1
    lot = n.parking_lots[0]
    ramp = n.on_ramps[0]

    assert lot.n_parked_cars == 0
    assert ramp.blocks == 0
    n.run(1000)
    assert lot.n_parked_cars > 10
    assert ramp.blocks > 10


def test_build_network():
    n = build_network(nodes, edges, entry_points, exit_points)
    assert len(n.intersections) == len(nodes)
    assert len(n.lanes) == len(edges)*2
    assert len(n.on_ramps) == len(entry_points)
    assert len(n.parking_lots) == len(exit_points)

    n.run(1000)
    for lot in n.parking_lots:
        assert lot.n_parked_cars > 0

from pytest import raises
from src.infinite_sample import InfiniteSample


def test_init():
    InfiniteSample([1, 2, 3], [1, 1, 1])
    InfiniteSample(range(3), range(3))

    with raises(ValueError):
        InfiniteSample([1], [2, 3])

    with raises(ValueError):
        InfiniteSample([], [])


def test_peak():
    sample = InfiniteSample([1, 2, 3], [1, 1, 1])
    for _ in range(10):
        peak_val = sample.peak()
        assert sample.pop() == peak_val


def test_sampling():
    sample = InfiniteSample([1, 2, 3], [1, 1, 1])
    vals = [sample.pop() for _ in range(1000)]
    assert set(vals) == {1, 2, 3}

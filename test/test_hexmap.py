import pytest

import geks


def test_item():
    hm = geks.RectHexmap(None, (5, 5))
    hm[2, 2] = "test_value"
    assert hm[2, 2] == hm.map[geks.Hex((2, 2))]
    assert hm[2, 2] != hm.map[geks.Hex((1, 3))]
    assert hm[geks.Hex((2, 2))] == hm.map[geks.Hex((2, 2))]


def test_keyerror():
    hm = geks.RectHexmap(True, (5, 5))
    assert hm.map[geks.Hex((2, 2))]
    with pytest.raises(KeyError):
        hm.map[geks.Hex((-2, -2))]
    with pytest.raises(KeyError):
        hm[-2, -2]


def test_mapped():
    hm = geks.RoundHexmap(None, 4)
    assert hm.is_mapped(geks.Hex((0, 1)))
    assert not hm.is_mapped(geks.Hex((0, 10)))


def test_neighbors():
    hm = geks.RectHexmap(None, (2, 2))
    assert len(hm.mapped_neighbors(geks.Hex((0, 0)))) == 2


def test_corners():
    width = 10
    height = 5
    hm = geks.RectHexmap(None, (width, height), flat=False)
    nw, ne, sw, se = hm.corners()
    assert geks.hex_distance(nw, ne) == width - 1
    assert geks.hex_distance(nw, sw) == height - 1

import pytest

import geks


def test_getitem():
    hm = geks.RectHexmap(None, (5, 5))
    hm.map[geks.Hex((2, 2))] = 'test_value'
    assert hm[2, 2] == hm.map[geks.Hex((2, 2))]
    assert hm[2, 2] != hm.map[geks.Hex((1, 3))]


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

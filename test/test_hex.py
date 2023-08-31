from geks import Hex


def test_math():
    assert Hex((1, 2)) - Hex((1, 3)) == Hex((0, 0)) + Hex((0, -1))


def test_norm():
    assert Hex((1, 2)).norm() == 3


def test_neighbor():
    he0 = Hex((4, 5))
    he = he0
    for di in range(6):
        he = he.neighbor(di)
    assert he == he0


def test_round():
    he1 = Hex((3.5, -5.5)).round()
    he2 = Hex((4, -6))
    assert he1 == he2

import geks


def test_distance():
    he1 = geks.Hex((-4, -12))
    he2 = geks.Hex((-9, 10))
    assert geks.hex_distance(he1, he2) == geks.hex_distance(he2, he1)


def test_line():
    he1 = geks.Hex((3, 2))
    he2 = geks.Hex((8, -2))
    line = geks.hex_line(he1, he2)
    assert he1 in line
    assert he2 in line
    assert geks.Hex((6, 0)) in line
    assert geks.Hex((5, 0)) in line


def test_ring():
    radius = 5
    center = geks.Hex((6, -2))
    ring = geks.hex_ring(center, radius)
    for he in ring:
        assert geks.hex_distance(he, center) == radius


def test_circle():
    radius = 5
    center = geks.Hex((34, -109))
    circle = geks.hex_circle(center, radius)
    for he in circle:
        assert geks.hex_distance(he, center) <= radius


def test_rotate():
    center = geks.Hex((-74, 29))
    he_0 = geks.Hex((4, 67))

    he_p1 = geks.hex_rotate(center, he_0, 1)
    he_m1 = geks.hex_rotate(center, he_0, -1)
    assert he_p1 != he_m1
    assert he_p1 == geks.hex_rotate(center, he_m1, 2)

    he_p2 = geks.hex_rotate(center, he_0, 2)
    assert he_p2 == geks.hex_rotate(center, he_p1, 1)

    he_p3 = geks.hex_rotate(center, he_0, 3)
    he_m3 = geks.hex_rotate(center, he_0, -3)
    assert he_m3 == he_p3

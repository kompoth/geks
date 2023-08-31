import geks


def test_conversion():
    lo = geks.Layout((8, 12), flat=True)
    center = geks.Hex((-5, 2))
    radius = 10
    circle = geks.hex_circle(center, radius)

    for he in circle:
        pixel = lo.hex2pixel(he)
        assert lo.pixel2hex(pixel) == he


def test_corners():
    lo = geks.Layout((3, 2), flat=False)
    he1 = geks.Hex((-5, 2))
    he2 = geks.Hex((-4, 2))
    corn1 = lo.hex_corners(he1)
    corn2 = lo.hex_corners(he2)
    common = set(tuple(x) for x in corn1) & set(tuple(x) for x in corn2)
    assert len(common) == 2

import geks


def test_heightmap():
    orig = geks.RectHexmap(None, (40, 20))
    calc = geks.RectHexmap(None, (40, 20))
    geks.gen_heightmap(calc)

    uncommon = [
        he
        for he in list(calc) + list(orig)
        if he not in calc.keys() or he not in orig.keys()
    ]
    assert not uncommon

    for he, val in calc.items():
        assert val is not None


def test_fill_sinks_py():
    hm = geks.RectHexmap(None, (40, 20))
    geks.gen_heightmap(hm)
    geks.fill_sinks_py(hm)


def test_fill_sinks_cy():
    hm = geks.RectHexmap(None, (40, 20))
    geks.gen_heightmap(hm)
    geks.fill_sinks_cy(hm)

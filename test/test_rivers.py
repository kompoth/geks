import geks


def test_river_centers():
    hm = geks.RectHexmap(None, (40, 20))
    geks.gen_heightmap(hm)
    geks.fill_sinks_cy(hm)
    geks.generate_rivers(hm, 5, -1, 150, edgify=False)


def test_river_edges():
    hm = geks.RectHexmap(None, (40, 20))
    geks.gen_heightmap(hm)
    geks.fill_sinks_cy(hm)
    geks.generate_rivers(hm, 5, -1, 150)

import geks


def test_a_star_wall():
    hm = geks.RectHexmap(False, dims=(3, 2), flat=True)
    hm[1, 0] = True
    start = geks.Hex((0, 0))
    target = geks.Hex((2, -1))
    path, nstep = geks.dijkstra_path(
        hm, start, target, distance=10, block_func=lambda y, x: hm.map[x]
    )
    assert nstep == 4
    assert len(path) == 5
    assert geks.Hex((1, 1)) in path


def test_a_star_rugged():
    hm = geks.RectHexmap(1, dims=(3, 2), flat=True)
    hm[1, 0] = 10
    hm[1, 1] = 3
    start = geks.Hex((0, 0))
    target = geks.Hex((2, -1))
    path, nstep = geks.dijkstra_path(
        hm, start, target, distance=10, cost_func=lambda y, x: hm.map[x]
    )
    assert nstep == 6
    assert len(path) == 5
    assert geks.Hex((1, 1)) in path


def test_a_star_distance():
    hm = geks.RectHexmap(1, dims=(10, 2), flat=True)
    start = geks.Hex((0, 0))
    target = geks.Hex((9, -3))
    path, nstep = geks.dijkstra_path(hm, start, target, distance=6)
    assert not path
    assert nstep is None


def test_a_star_unavailable():
    hm = geks.RoundHexmap(False, 10)
    blocked = [(-8, 7), (-8, 8), (-7, 8), (-6, 7), (-6, 6), (-7, 6)]
    for qr in blocked:
        hm[qr] = True

    start = geks.Hex((0, 0))
    target = geks.Hex((-7, 7))
    path, nstep = geks.dijkstra_path(
        hm, start, target, distance=100, block_func=lambda y, x: hm.map[x]
    )
    assert not path
    assert nstep is None

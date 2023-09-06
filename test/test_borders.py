import geks


def test_edge_equal():
    he = geks.Hex((0, 0))
    di = geks.Hex((1, 1))
    edge0 = geks.HexEdge(he, di, 1)

    ne = he + di 
    edge1 = geks.HexEdge(ne, he - ne, 1)
    assert edge0 == edge1

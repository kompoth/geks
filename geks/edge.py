class HexEdge:
    def __init__(self, he, di, rot):
        self.he = he
        self.di = di
        self.rot = rot

    def __eq__(self, rs):
        eq = self.he == rs.he and self.di == rs.di
        adj = self.he == rs.he + rs.di and self.he + self.di == rs.he
        return eq or adj

"""
Class for an abstract hexagon object.
"""
import numpy as np


# Directions to hexagon neighbors
NEIGHBORS = np.array(((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)))


class Hex:
    def __init__(self, pos=None):
        self.pos = np.array(pos)

    def __repr__(self):
        return f"<Hex: {self.q}, {self.r}>"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return np.all(self.pos == other.pos)

    def __lt__(self, other):
        return np.all(self.pos < other.pos)

    def __add__(self, other):
        return Hex(self.pos + other.pos)

    def __sub__(self, other):
        return Hex(self.pos - other.pos)

    def __mul__(self, mul):
        return Hex(self.pos * mul)

    def norm(self):
        """Returns a distance to Hex((0, 0))."""
        abs_s = abs(self.pos.sum())
        return round((np.fabs(self.pos).sum() + abs_s) * 0.5)

    def neighbor(self, direction):
        """Returns neighbor in given direction."""
        return self + Hex(NEIGHBORS[direction])

    def neighbors(self, cond=lambda x: True):
        """Returns all neighbors."""
        res = []
        for di in range(6):
            ne = self.neighbor(di)
            if cond(ne):
                res.append(ne)
        return res

    def round(self):
        """Rounds hexagon coordinates to closest integers."""
        return Hex(np.rint(self.pos).astype("int"))

    @property
    def q(self):
        return self.pos[0]

    @property
    def r(self):
        return self.pos[1]

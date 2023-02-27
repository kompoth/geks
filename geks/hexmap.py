import copy
import numpy as np

from .hexagon import Hex
from .utils import hex_circle

class Hexmap:
    """Class for a space of hexagons."""
    def __init__(
        self, default, radius=None, dims=None, 
        rect=True, flat=True
    ):
        self.map = {}
        if radius:
            zero = Hex((0, 0))
            for he in hex_circle(zero, radius):
                self.map[he] = copy.copy(default)
        elif dims:
            # This is slightly faster then two nested for-loops
            grid = np.array(
                np.meshgrid(range(dims[0]), range(dims[1]))
            ).T.reshape(-1, 2)
            if flat:
                grid[:, 1] -= grid[:, 0] // 2
            else:
                grid[:, 0] -= grid[:, 1] // 2
            for pos in grid:
                self.map[Hex(pos)] = copy.copy(default)
        else:
            raise ValueError("Provide either 'radius' or 'dims' parameter.")

    def __getitem__(self, pos):
        return self.map[Hex(pos)]

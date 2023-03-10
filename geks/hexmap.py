import copy
import numpy as np

from .hexagon import Hex
from .geometry import hex_circle, hex_distance


class Hexmap:
    """Base class for a hexagonal map data structure."""
    def __init__(self):
        self.map = {}

    def __getitem__(self, pos):
        return self.map[Hex(pos)]
    
    def __setitem__(self, pos, value):
        self.map[Hex(pos)] = value
    
    def is_mapped(self, he):
        return he in self.map
    

class RoundHexmap(Hexmap):
    """Round hexagonal map."""
    def __init__(self, default, radius):
        """Constructor for a round hexagonal map.

        Parameters
        ----------
        default : any
            Any piece of data that should be stored in a hexagon by
            default.
        radius : int
            Radius of the map to be constructed.
        """
        super().__init__()
        self.radius = radius

        zero = Hex((0, 0))
        for he in hex_circle(zero, radius):
            self.map[he] = copy.copy(default)

    

class RectHexmap(Hexmap):
    def __init__(self, default, dims, flat=True):
        """Constructor for a rectangular hexagonal map.

        Parameters
        ----------
        default : any
            Any piece of data that should be stored in a hexagon by
            default.
        dims : iterable(int)
            Lengths of map's edges.
        flat : bool, default: True
            If True, flat top hexagonal system is used, pointy otherwise.
        """
        super().__init__()
        self.dims = dims
        self.flat = flat

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

    def corners(self):
        """Returns corner hexagons of a map."""
        width = self.dims[0]
        height = self.dims[1]
        if self.flat:
            r_offset = (width - 1) // 2
            nw = Hex((0, 0))
            ne = Hex((width - 1, - r_offset))
            sw = Hex((0, height - 1))
            se = Hex((width - 1, - r_offset + height - 1))
        else:
            q_offset = (height - 1) // 2
            nw = Hex((0, 0))
            ne = Hex((width - 1, 0))
            sw = Hex((- q_offset, height - 1))
            se = Hex((- q_offset + width - 1, height - 1)) 
        return (nw, ne, sw, se)

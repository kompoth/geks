import copy
import numpy as np

from .hexagon import Hex
from .geometry import hex_circle


class Hexmap:
    """Base data structure for a collection of hexagons."""
    def __init__(self, default, radius=None, dims=None, flat=True):
        """
        Constructor. Can build a hexagonal (round) or rectangular map.
        map.

        Parameters
        ----------
        default : any
            Any piece of data that should be stored in a hexagon by
            default.
        radius : int, default: None
            Radius of a hexagonal map. If not None, a round map will be
            built. One of 'radius' or 'dims' must be provided.
        dims : iterable(int), default: None
            Lengths of angled map edges. If not None, a rectangular map
            will be built. One of 'radius' or 'dims' must be provided.
        flat : bool, default: True
            If True, map is constructed for flat top haxagons. Neccessary
            only for rectangular maps.
        """
        # Build map
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

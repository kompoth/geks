import numpy as np

from .hexagon import Hex


THIRTY_GRAD = 0.52
H2P = np.array((
    (              1.5,        0.),
    (0.5 * np.sqrt(3.), np.sqrt(3.))
))
P2H = np.array((
    (  2. / 3.,               0.),
    (- 1. / 3., np.sqrt(3.) / 3.)
))
CORNERS = np.array((
    ( 1.00,  0.00),
    ( 0.50,  0.87),
    (-0.50,  0.87),
    (-1.00,  0.00),
    (-0.50, -0.87),
    ( 0.50, -0.87)
))


class Layout:
    """Screen layout of hexagons."""
    def __init__(self, size=(1, 1), flat=True):
        self.size = np.array(size)
        bypass = 1 if flat else -1

        # Conversion matrices
        self.h2p = H2P[::bypass, ::bypass]
        self.p2h = P2H[::bypass, ::bypass]
        # Corner directions
        self.corners = self.size * CORNERS[:, ::bypass]

    def hex2pixel(self, he):
        """Convert screen coordinates to hexagonal."""
        return self.h2p.dot(he.pos) * self.size
    
    def pixel2hex(self, xy):
        """Convert hexagonal coordinates to screen."""
        return Hex(self.p2h.dot(xy / self.size)).round()

    def hex_corners(self, he):
        """Calculate screen coordinates of hexagon's corners."""
        center = self.hex2pixel(he)
        angles = np.tile(center, (6, 1)) + self.corners
        return angles

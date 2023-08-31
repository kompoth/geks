import numpy as np

from .hexagon import Hex
from .geometry import hex_rotate


SQRT3 = np.sqrt(3.0)
H2P = np.array(((1.5, 0.0), (0.5 * SQRT3, SQRT3)))
P2H = np.array(((2.0 / 3.0, 0.0), (-1.0 / 3.0, SQRT3 / 3.0)))
CORNERS = np.array(
    (
        (1.0, 0.0),
        (0.5, 0.5 * SQRT3),
        (-0.5, 0.5 * SQRT3),
        (-1.0, 0.00),
        (-0.5, -0.5 * SQRT3),
        (0.5, -0.5 * SQRT3),
    )
)


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
        corners = np.tile(center, (6, 1)) + self.corners
        return corners

    def hex_edge(self, edge):
        """Calculate edge coordinates"""
        v1 = self.h2p.dot(edge.di.pos)
        v2 = np.empty_like(v1)
        v2[0] = -v1[1]
        v2[1] = v1[0]
        v2 = v2 * 0.5 / np.linalg.norm(v2)
        p0 = self.h2p.dot(edge.he.pos) + v1 * 0.5
        pts = np.array([p0 - v2, p0 + v2]) * self.size

        hen = hex_rotate(edge.he, edge.he + edge.di, edge.rot)
        ptn = self.hex2pixel(hen)
        dists = np.array([np.linalg.norm(ptn - pt) for pt in pts])
        args = np.argsort(dists, axis=0)[::-1]
        pts = pts[args]
        return pts

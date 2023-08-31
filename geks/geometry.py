"""
Geometrical operations with hexagons
"""
import numpy as np

from .hexagon import Hex


def hex_distance(he1, he2):
    """Returns distance between two hexagons in steps"""
    return (he2 - he1).norm()


def hex_line(he1, he2):
    """Returns line in hexagonal space"""
    norm = hex_distance(he1, he2)
    coords = np.linspace(he1.pos, he2.pos, round(norm) + 1)
    return [Hex(c).round() for c in coords]


def hex_ring(center, radius):
    """Returns a ring of hexagons"""
    ring = []
    he = center
    for i in range(radius):
        he = he.neighbor(4)
    for direction in range(6):
        for curve in range(radius):
            ring.append(he)
            he = he.neighbor(direction)
    return ring


def hex_circle(center, radius):
    """Returns a circle of hexagons"""
    circle = [center]
    for layer in range(1, radius + 1):
        circle += hex_ring(center, layer)
    return circle


def hex_rotate(center, he, n=1):
    """Rotate hexagon on 60 * n"""
    vec = he - center
    pos = np.append(vec.pos, -vec.q - vec.r)
    pos = (-1) ** n * np.roll(pos, n)
    vec.pos = pos[:2]
    return (center + vec).round()

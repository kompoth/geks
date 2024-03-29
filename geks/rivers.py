"""Rivers generation"""
from .pathfinding import dijkstra_scan, extract_path
from .geometry import hex_rotate, hex_circle
from .edge import HexEdge

import random


def gen_river_path(hm, source, ocean_alt):
    """Wrapper for Dijkstra method to find fastest path to ocean"""
    preds, costs = dijkstra_scan(
        hm,
        source,
        block_unmapped=False,
        block_func=lambda cur, ne: hm[cur] < hm.get(ne, 0),
        break_func=lambda cur, ne: ne not in hm or hm[ne] <= ocean_alt,
        priority_func=lambda ne, d, i: hm[ne],
    )

    estuary = None
    for he in preds.keys():
        if he not in hm or hm[he] <= ocean_alt:
            estuary = he
            break
    if estuary is None:
        raise RuntimeError("Failed to reach ocean")

    path = extract_path(preds, source, estuary)
    if path is None:
        raise RuntimeError("Failed to build river path")
    return path


def gen_river_edges(hm, river, ocean_alt, curv=None):
    """
    Generates a list of hex edges from a hexagon list that
    describes river path
    """
    edges = []
    hc = river[0]
    rot = 1 if random.random() < 0.5 else -1
    hr = hex_rotate(hc, river[1], -rot)
    edges.append(HexEdge(hc, hr - hc, rot))

    if curv is None:
        curv = 0.1
        curv_step = (1.0 - curv * 2) / len(river)
    else:
        curv_step = 0.0
    step = 1
    done = False
    while step + 1 < len(river) and not done:
        hr = hc
        hc = river[step]

        for nrot in range(5):
            hr = hex_rotate(hc, hr, rot)
            done = hr not in hm or hm[hr] <= ocean_alt
            if hr == river[step + 1] or done:
                break
            else:
                edges.append(HexEdge(hc, hr - hc, rot))

        if nrot == 5:
            raise RuntimeError(f"Too many rotations: {nrot}")
        if random.random() < curv and not done and nrot < 4:
            edges.append(HexEdge(hc, hr - hc, rot))
            rot = -1 * rot
        step += 1
        curv += curv_step
    return edges


def generate_rivers(
    hm,
    num_rivers,
    ocean_alt,
    source_min_alt,
    source_min_dist=2,
    edgify=True,
    curv=None,
):
    """
    Generates rivers from the given minimal altitude to the ocean level or the
    map's edges.

    Parameters
    ----------
    hm : hexmap.Hexmap
        Collection of hexagons, containing numeric altitudes
    num_rivers : int
        Number of rivers to generate
    ocean_alt : int
        Ocean level
    source_min_alt : int
        Minimal altitude of river sources
    source_min_dist : int, default: 2
        Minimal distance between river sources
    edgify : bool, default: True
        Plot rivers through hexagons' edges
    curv : int or None, default: None
        If None, edgified river curvature increases as river gets closer to
        the ocean. Otherwise curvature will be fixed, the higher the value is.
    """
    # Prepare pool of points that can be river sources
    pool = [
        he
        for he, alt in hm.items()
        if alt > source_min_alt and len(hm.mapped_neighbors(he)) == 6
    ]

    # Generate river paths
    it = 0
    rivers = []
    while it < num_rivers and pool:
        source = random.choice(pool)
        river = gen_river_path(hm, source, ocean_alt)
        rivers.append(river)
        busy = [he for he in river] + hex_circle(source, source_min_dist)
        pool = [he for he in pool if he not in busy]
        it += 1

    if not edgify:
        return rivers

    # Direct rivers through edges of hexagons and handle mergers
    all_edges = []
    for river in rivers:
        river_edges = gen_river_edges(hm, river, ocean_alt)
        for nit, edge in enumerate(river_edges):
            if edge in [ed for sublist in all_edges for ed in sublist]:
                river_edges = river_edges[:nit]
                break
        all_edges.append(river_edges)
    return all_edges

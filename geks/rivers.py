"""Rivers generation"""
from .pathfinding import dijkstra_scan, extract_path
from .geometry import hex_rotate
from .edge import HexEdge

import random


def gen_river_path(hm, source, ocean_lvl):
    """Wrapper for Dijkstra method to find fastest path to ocean"""
    preds, costs = dijkstra_scan(
        hm,
        source,
        block_unmapped=False,
        block_func=lambda cur, ne: hm[cur] < hm.map.get(ne, 0),
        break_func=lambda cur, ne: not hm.is_mapped(ne) or hm[ne] <= ocean_lvl,
        priority_func=lambda ne, d, i: hm[ne],
    )

    estuary = None
    for he in preds.keys():
        if not hm.is_mapped(he) or hm[he] <= ocean_lvl:
            estuary = he
            break
    if estuary is None:
        raise RuntimeError("Failed to reach ocean")

    path = extract_path(preds, source, estuary)
    if path is None:
        raise RuntimeError("Failed to build river path")
    return path


def gen_river_edges(hm, river, ocean_lvl, w=0.5):
    """
    Generates a list of hex edges from a hexagon list that
    describes river path
    """
    edges = []
    hc = river[0]
    rot = 1 if random.random() < 0.5 else -1
    hr = hex_rotate(hc, river[1], -rot)
    edges.append(HexEdge(hc, hr - hc, rot))

    step = 1
    done = False
    while step + 1 < len(river) and not done:
        hr = hc
        hc = river[step]

        for nrot in range(5):
            hr = hex_rotate(hc, hr, rot)
            done = not hm.is_mapped(hr) or hm[hr] <= ocean_lvl
            if hr == river[step + 1] or done:
                break
            else:
                edges.append(HexEdge(hc, hr - hc, rot))

        if nrot == 5:
            raise RuntimeError(f"Too many rotations: {nrot}")
        if random.random() < w and not done:
            edges.append(HexEdge(hc, hr - hc, rot))
            rot = -1 * rot
        step += 1
    return edges

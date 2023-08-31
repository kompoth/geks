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
        block_func=lambda cur, ne: hm[cur] < hm.get(ne, 0),
        break_func=lambda cur, ne: ne not in hm or hm[ne] <= ocean_lvl,
        priority_func=lambda ne, d, i: hm[ne],
    )

    estuary = None
    for he in preds.keys():
        if he not in hm or hm[he] <= ocean_lvl:
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
            done = hr not in hm or hm[hr] <= ocean_lvl
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


#def generate_rivers(
#    hm,
#    num_rivers,
#    ocean_alt=0.50,
#    source_min_alt=0.90,
#    edgify=True
#):
#    # Prepare pool of points that can be river sources
#    pool = [he for he, alt in hm.items() if alt > source_alt]
#
#    # Generate river paths
#    step = 0
#    rivers = []
#    while step < num_rivers and pool:
#        src = random.choice(pool)
#        river = geks.gen_river_path(hm, src, ocean_lvl)
#        rivers.append(river)
#        busy = [he for he in river] + geks.hex_circle(src, 2)
#        pool = [he for he in pool if he not in busy]
#        step += 1


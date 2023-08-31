"""Pathfinding routines."""
from heapq import heappop, heappush

from .geometry import hex_distance


def extract_path(predecessors, start, target):
    """
    Builds a path to the target from thr predecessors dict.

    Parameters
    ----------
    predecessors : dict of hexagon.Hex
        Maps each reached hexagon with its predecessor
    start : hexagon.Hex
        Start hexagon
    target : hexagon.Hex
        Target hexagon

    Returns
    -------
    list of hexagon.Hex or None
        Path to target hexagon
    """
    if target not in predecessors:
        return None
    trace = [target]
    he = target
    while he != start:
        trace.append(predecessors[he])
        he = predecessors[he]
    return trace[::-1]


def dijkstra_scan(
    hm,
    start,
    distance=100,
    block_unmapped=True,
    block_func=lambda he, nhe: False,
    cost_func=lambda he, nhe: 1,
    break_func=lambda he, nhe: False,
    priority_func=None,
):
    """
    Finds available hexagons in given range.

    Parameters
    ----------
    hm : hexmap.Hexmap
        Collection of hexagons
    start : hexagon.Hex
        Starting hexagon
    distance : int, dafault: 100
        Distance limit
    block_unmapped : bool, default: True
        Assume unmapped hexagons as blocked
    block_func : callable, default: none blocked
        Takes current and next hexagon, returns True if a hexagon is
        blocked
    cost_func : callable, default: 1 for all hexagons
        Takes current and next hexagon, returns cost of step over a
        hexagon
    break_func : callable, default: exit normally
        Takes current and next hexagon, returns True when the scan loop
        must be broken
    priority_func : callable, default: steps to reach hexagon
        Takes hexagon, distance to it and number of iteration, returns
        priority value (smallest is first)

    Returns
    -------
    dict of hexagon.Hex
        Maps each reached hexagon with its predecessor
    dict of int or float
        Coast of getting to each reached hexagon
    """
    if start not in hm.map:
        raise ValueError(f"Hexagon '{start}' is not mapped.")

    predecessors = {start: None}
    costs = {start: 0}
    frontier = []
    heappush(frontier, (0, start))

    it = 0  # Number of iterations
    while frontier:
        it += 1
        he = heappop(frontier)[1]
        for nhe in he.neighbors():
            # Continue if hex already visited or unavailable
            off_bounds = block_unmapped and nhe not in hm.map
            if off_bounds or block_func(he, nhe) or nhe in predecessors:
                continue
            # Calculate steps
            steps = costs[he] + cost_func(he, nhe)
            if steps > distance:
                continue
            predecessors[nhe] = he
            costs[nhe] = steps
            # Break on user defined condition
            if break_func(he, nhe):
                return predecessors, costs
            # Determine priority
            if priority_func:
                priority = priority_func(nhe, steps, it)
            else:
                priority = steps
            heappush(frontier, (priority, nhe))
    return predecessors, costs


def dijkstra_path(
    hm,
    start,
    target,
    distance=100,
    block_func=lambda he, nhe: False,
    cost_func=lambda he, nhe: 1,
    algoritm="a_star",
):
    """
    Find a path to a hexagon.

    Parameters
    ----------
    hm : hexmap.Hexmap
        Collection of hexagons
    start : hexagon.Hex
        Starting hexagon
    target : hexagon.Hex
        Target hexagon
    distance : int, dafault: 100
        Distance limit
    block_func : callable, default: none blocked
        Takes current and next hexagon, returns True if a hexagon is
        blocked
    cost_func : callable, default: 1 for all hexagons
        Takes current and next hexagon, returns cost of step over a
        hexagon
    algoritm : str, default: "a_star"
        Possible options are "full_scan", "a_star", "greedy"

    Returns
    -------
    list of hexagon.Hex or None
        Path to target hexagon
    int or None
        Total cost of a resulting path
    """
    if target not in hm.map:
        raise ValueError(f"Hexagon '{target}' is not mapped.")

    if algoritm == "a_star":

        def priority_func(x, s, i):
            return hex_distance(x, target) + s

    elif algoritm == "greedy":

        def priority_func(x, s, i):
            return hex_distance(x, target)

    else:
        priority_func = None

    preds, costs = dijkstra_scan(
        hm,
        start,
        distance,
        block_func=block_func,
        cost_func=cost_func,
        break_func=lambda x, y: x == target,
        priority_func=priority_func,
    )

    path = extract_path(preds, start, target)
    if path is None:
        cost = None
    else:
        cost = costs[target]
    return path, cost

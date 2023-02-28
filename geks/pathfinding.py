"""Pathfinding routines."""
from heapq import heappop, heappush

from .geometry import hex_distance


def dijkstra_scan(
    hm, start, distance=100, 
    block_func=lambda x: False,
    cost_func=lambda x: 1,
    break_func=lambda x: False,
    priority_func=None
):
    """
    Finds available hexagons in given range.
    
    Parameters
    ----------
    hm : hexmap.Hexmap
        Collection of hexagons.
    start : hexagon.Hex 
        Starting hexagon.
    distance : int, dafault: 100
        Distance limit.
    block_func : callable, default: none blocked
        Takes hexagon, returns True if a hexagon is blocked.
    cost_func : callable, default: 1 for all hexagons
        Takes hexagon, returns cost of step over a hexagon.
    break_func : function, default: exit normally
        Takes hexagon, returns True if BFS loop must be broken.
    priority_func : callable, default: steps to reach hexagon
        Takes hexagon, distance to it and iteration, returns priority.
        value (smallest is first)

    Returns
    -------
    dict[hexagon.Hex, hexagon.Hex]
        Mapping of predecessors, from which a trace can be constructed
    """
    if start not in hm.map:
        raise ValueError(f"Hexagon '{start}' is not mapped.") 

    traces = {}
    traces[start] = (None, 0)
    frontier = []
    heappush(frontier, (0, start))
    
    it = 0
    while frontier:
        it += 1
        he = heappop(frontier)[1]
        for nhe in he.neighbors():
            # Continue if hex already visited or unavailable
            if nhe not in hm.map or block_func(nhe) or nhe in traces:
                continue
            # Calculate steps
            steps = traces[he][1] + cost_func(nhe)
            if steps > distance:
                continue
            traces[nhe] = (he, steps)
            # Break on user defined condition
            if break_func(nhe):
                return traces
            # Determine priority
            if priority_func:
                priority = priority_func(nhe, steps, it)
            else:
                priority = steps
            heappush(frontier, (priority, nhe))
    return traces


def dijkstra_path(
    hm, start, target, distance=100,
    block_func=lambda x: False,
    cost_func=lambda x: 1,
    algoritm="fast"
):
    """
    Find a path to a hexagon.

    Parameters
    ----------
    hm : hexmap.Hexmap
        Collection of hexagons.
    start : hexagon.Hex 
        Starting hexagon.
    target : hexagon.Hex 
        Target hexagon.
    distance : int, dafault: 100
        Distance limit.
    block_func : callable, default: none blocked
        Takes hexagon, returns True if a hexagon is blocked.
    cost_func : callable, default: 1 for all hexagons
        Takes hexagon, returns cost of step over a hexagon.
    algoritm : str, default: "a_star"
        Possible options are "full_scan", "a_star", "greedy".

    Returns
    -------
    list[hexagon.Hex]
        Path to target hexagon.
    int
        Total cost of a resulting path.
    int
        Number of pathfinding iterations.
    """
    if target not in hm.map:
        raise ValueError(f"Hexagon '{target}' is not mapped.") 

    if algoritm == "a_star":
        priority_func = lambda x, s, i: hex_distance(x, target) + s
    elif algoritm == "greedy":
        priority_func = lambda x, s, i: hex_distance(x, target) 
    elif algoritm == "full_scan":
        priority_func = None
    else:
        raise ValueError(f"Unknown algoritm '{algoritm}'.")
        
    traces = dijkstra_scan(
        hm, start, distance, 
        block_func=block_func,
        cost_func=cost_func,
        break_func=lambda x: x == target,
        priority_func=priority_func
    )
    
    if target not in traces:
        return None, None, None
    trace = [target]
    he = target
    while he != start:
        trace.append(traces[he][0])
        he = traces[he][0]
    return trace[::-1], traces[target][1], len(traces)


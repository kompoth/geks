import random
import copy
import numpy as np

from .geometry import hex_distance, hex_circle
from .cython import fill_sinks


def gen_heightmap(hm, sk=0.5, max_alt=255, seed=None):
    """
    Fills hexmap 'hm' with altitudes. Caution: overwrites original values.

    Parameters
    ----------
    hm : hexmap.Hexmap
        Collection of hexagons
    sk : float
        Determines terrain smoothness
    max_alt : int
        Maximum altitude.
    seed : list[int], optional
        Altitudes for 7 initial tiles
    """
    # Calculate number of iterations
    corners = hm.corners()
    cent = hm.center()
    diag = max([hex_distance(cent, co) for co in corners])
    np2 = int(diag - 1).bit_length()

    # Prepare seed altitudes
    random.seed()
    if seed is None:
        seed = [random.randint(0, max_alt) for i in range(7)]
    elif len(seed) != 7:
        raise ValueError("Need exactly 7 seed values.")
    initial = [cent] + cent.neighbors()
    known = {he: val for he, val in zip(initial, seed)}

    num_target = len(hm)
    h_var = max_alt
    num_it = 1
    done = False
    while not done and num_it <= np2:
        # Expand calculated map, set anchor points
        known = {(he - cent) * 2 + cent: val for he, val in known.items()}
        anchors = copy.copy(known)

        # Set a list of points to be calculated in current iteration
        unknown = set(hex_circle(cent, 2**num_it)) - set(known.keys())
        unknown = [he for he in unknown if he in hm]

        # Calculate unknown
        num_ready = sum((1 if he in hm else 0 for he in known))
        while not done and unknown:
            he = unknown.pop()
            mean = sum((anchors.get(ne, 0) for ne in he.neighbors())) // 2
            alt = mean + random.randint(0, h_var) - h_var // 2
            known[he] = alt
            num_ready += 1
            if num_ready >= num_target:
                done = True
        h_var = int(h_var * sk)
        num_it += 1

    alts = dict(filter(lambda pair: pair[0] in hm, known.items()))
    min_r = min(alts.values())
    max_r = max(alts.values())
    for he, val in alts.items():
        if he in hm:
            norm_val = (val - min_r) * max_alt / (max_r - min_r)
            hm[he] = round(norm_val)


def fill_sinks_py(hm, eps=1):
    """
    Python implementation of Planchon-Darboux method to remove isolated
    sinks from a height map.

    Parameters
    ----------
    hm : hexmap.Hexmap
        Collection of hexagons with given altitudes
    eps : int, default: 1
        Elevation parameter
    """
    hm0 = copy.deepcopy(hm)
    inf = np.max([h for he, h in hm0.items()])

    # Step 1: fill with water
    for pt, alt in hm.items():
        hm[pt] = alt if hm.is_edge(pt) else inf

    # Step 2: remove excess
    proceed = True
    while proceed:
        proceed = False
        order = list(hm.keys())[::-1]
        for pt in order:
            if hm0.is_edge(pt) or hm0[pt] == hm[pt]:
                continue
            for ne in pt.neighbors():
                alt = hm[ne] + eps
                if hm0[pt] >= alt:
                    hm[pt] = hm0[pt]
                    proceed = True
                    break
                elif hm[pt] > alt and alt > hm0[pt]:
                    hm[pt] = alt
                    proceed = True


def fill_sinks_cy(hm, eps=1):
    """
    Binding to Cython implementation of Planchon-Darboux method.

    Parameters
    ----------
    hm : hexmap.Hexmap
        Collection of hexagons with given altitudes
    eps : int, default: 1
        Elevation parameter
    """
    # Fastest way to determine boundaries
    pts = np.array([(he.q, he.r) for he in hm])
    qmin, qmax = np.min(pts[:, 0]), np.max(pts[:, 0])
    rmin, rmax = np.min(pts[:, 1]), np.max(pts[:, 1])
    qsize = qmax - qmin + 1
    rsize = rmax - rmin + 1

    # Prepare matrices
    alts0 = np.ndarray((qsize, rsize))
    edges = np.ndarray((qsize, rsize), dtype=np.dtype("i"))
    alts0[:] = np.nan
    for he in hm:
        alts0[he.q - qmin, he.r - rmin] = hm[he]
        edges[he.q - qmin, he.r - rmin] = hm.is_edge(he)

    # Run Cython
    inf = np.max([h for he, h in hm.items()])
    alts = fill_sinks(alts0, edges, inf, eps)

    # Fill hm with new values
    for he in hm:
        hm[he] = round(alts[he.q - qmin, he.r - rmin])


def altitude_cdf(hm):
    """
    For the given hexmap return its altitude CDF. Can be used for setting
    ocean level.

    Parameters
    ----------
    hm : hexmap.Hexmap
        Collection of hexagons with given altitudes
    """
    alts, freqs = np.unique(list(hm.values()), return_counts=True)
    distr = np.zeros(max(alts) + 1, dtype=int)
    np.put(distr, alts, freqs)
    cdf = np.cumsum(distr)
    cdf = cdf / len(hm)
    return cdf

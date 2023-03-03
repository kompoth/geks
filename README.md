# Geks - hexagonal maps package
Geks implements basic operations in a plain hexagonal space neccessary for
creating maps of hexagonal tiles. It also allows to build paths between tiles
using some well known algorithms.

In some time Geks might be converted to a more specific map generation project.

## Coordinate system
This package uses 
[axial approach](https://www.redblobgames.com/grids/hexagons/#coordinates)
which allows to use cartesian operators with minor changes. It uses two
coordinates, _q_ and _r_. Orientation of _q_ and _r_ axes slightly differs for
flat and pointy top hexagons.
![axes](pics/axes.svg)

Conversions between hexagonal and screen coordinates are implemented by
methods `hex2pixel` and `pixel2hex` of a `Layout` class.

## Pathfinding
At this point Geks can calculate a path between two mapped hexagons using
[Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm),
[A\* method](https://en.wikipedia.org/wiki/A*_search_algorithm) and
[greedy search](https://en.wikipedia.org/wiki/Greedy_algorithm).
The first approach is useful for determining all possible movement options
for a given hexagon. A* method is more efficient for a targeted pathfinding.
Greedy search is usually more efficient than A* in terms of calculation time
but may result in an inefficient solution.

These methods share the same basic concept. Therefore there are no separate
functions for them, all three algorithms are built on top of the same
`dijkstra_scan` function with different parameters. Use `dijkstra_path` to
build a path to a specific tile (A* is used by default) and `dijkstra_scan`
to determine all possible movement options.

On the following image green hexagons denote rugged terrain, grey tiles are
impassable walls.
![paths](pics/paths.svg)

User may determine cost of movement over each hexagon (e.g. travel time) and
what hexagons are blocked for trespassing (e.g. have walls on them).

## Requirements
Written on Python 3 (tested with v3.10.9).

Geks uses following packages not included in the standard library:
- `numpy` (tested with v1.23.5)
- `pytest` (optional, tested with v7.2.1)
- `matplotlib` (optional, tested with v3.6.2)

## Credits
Articles by [Red Blob Games](https://www.redblobgames.com/) on grids,
pathfinding and many other 



This package is mostly based on the theory from [Red Blob Games articles]().

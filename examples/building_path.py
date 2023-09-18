"""
Usage example showing how to map hexagons with different properties,
calculate path and rendering result with a debug front end.
"""
import matplotlib.pyplot as plt

import geks
from geks.front import FrontMPL

# Create rectangular map of unblocked hexagons with pointy top
default_value = {"price": 1, "blocked": False}
hm = geks.RectHexmap(default_value, dims=(12, 8), flat=True)

# Initialize convertion to screen coordinates and front end
layout = geks.Layout(flat=True)
mpl = FrontMPL(layout)

# Set walls
blocked = [(7, 1), (7, 0), (7, -1), (6, -1), (6, 2), (5, 2), (5, 3), (5, 4)]
for bl in blocked:
    hm[bl]["blocked"] = True

# Set rugged terrain by drawing a circle
swamps = geks.hex_circle(geks.Hex((3, 0)), 1)
for sw in swamps:
    if sw in hm:
        hm[sw]["price"] = 5

# Draw hexagons according to their values
for he, value in hm.items():
    mpl.plot_hex(
        he,
        fill=value["blocked"] or value["price"] > 1,
        facecolor="grey" if value["blocked"] else "lightgreen",
        edgecolor="black",
    )

# Highlight start and target hexagons
start = geks.Hex((0, 0))
target = geks.Hex((11, 2))
mpl.plot_hex(start, facecolor="lightblue")
mpl.plot_hex(target, facecolor="orange")

# Build path
path, nstep = geks.dijkstra_path(
    hm,
    start,
    target,
    distance=40,
    block_func=lambda y, x: hm[x]["blocked"],  # walls condition
    cost_func=lambda y, x: hm[x]["price"],  # cost of movement
)
mpl.plot_path(path, lw=2, color="darkblue")

# Save resulting image
mpl.fig.set_size_inches(10, 8)
plt.gca().invert_yaxis()
plt.autoscale(enable=True)
plt.savefig("example.png")

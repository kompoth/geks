import geks
from geks.front import FrontMPL
import numpy as np
import random

# Prepare height map
hm = geks.RoundHexmap(0, 32)
geks.gen_heightmap(hm, 0.6, seed=(255, 0, 0, 0, 0, 0, 0))
geks.fill_sinks_cy(hm)

# Set ocean level
cdf = geks.altitude_cdf(hm)
ocean_lvl = np.argmax(cdf > 0.5)

# Prepare graphical front end
layout = geks.Layout(flat=False)
mpl = FrontMPL(layout)

# Render height map
mpl.plot_hexmap(hm, ("#1F3C41", "#3B727C"), lambda x: hm[x] > ocean_lvl)
mpl.plot_hexmap(
    hm, ("#D1BE9D", "#B9A37E", "#64513B"), lambda x: hm[x] <= ocean_lvl
)

# Prepare pool of points that can be river sources
pool = [he for he, alt in hm.map.items() if cdf[alt] > 0.90]

# Generate 10 rivers
step = 0
all_rivers = []
while step < 10 and pool:
    src = random.choice(pool)
    river = geks.gen_river_path(hm, src, ocean_lvl)
    all_rivers.append(river)
    busy = [he for he in river] + geks.hex_circle(src, 2)
    pool = [he for he in pool if he not in busy]
    step += 1

    # Draw initial river path
    mpl.plot_path(river)

# Direct rivers through edges of hexagons and handle mergers
all_edges = []
for river in all_rivers:
    edges = geks.gen_river_edges(hm, river, ocean_lvl)
    for nit, edge in enumerate(edges):
        if edge in all_edges:
            edges = edges[:nit]
            break
    all_edges += edges
    # Draw river
    mpl.plot_border(edges, color="#1F3C41", width=1.2)
del all_edges

mpl.show()

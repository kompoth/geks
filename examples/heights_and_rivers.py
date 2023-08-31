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
ocean_alt = np.argmax(cdf > 0.5)
source_min_alt = np.argmax(cdf > 0.9)

# Prepare graphical front end
layout = geks.Layout(flat=False)
mpl = FrontMPL(layout)

# Render height map
mpl.plot_hexmap(hm, ("#1F3C41", "#3B727C"), lambda x: hm[x] > ocean_alt)
mpl.plot_hexmap(
    hm, ("#D1BE9D", "#B9A37E", "#64513B"), lambda x: hm[x] <= ocean_alt
)

# Generate 10 rivers
for edges in geks.generate_rivers(hm, 10, ocean_alt, source_min_alt):
    mpl.plot_border(edges, color="#1F3C41", width=1.2)

mpl.show()

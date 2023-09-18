import numpy as np
import matplotlib.pyplot as plt

import geks
from geks.front import FrontMPL

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
    mpl.plot_border(edges, color="#1F3C41", lw=1.2)

# Save resulting image
mpl.fig.set_size_inches(16, 16)
plt.gca().invert_yaxis()
plt.autoscale(enable=True)
plt.savefig("example.png", transparent=True)

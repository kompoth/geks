"""
A simple frontend based on matplotlib written for debug purposes
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


class FrontMPL:
    """A class that encapsulates matplotlib frontend"""

    def __init__(self, layout):
        """Constructor"""
        self.layout = layout
        self.fig, self.ax = plt.subplots(1)
        self.ax.set_aspect("equal")

        self.ax.set_yticklabels([])
        self.ax.set_xticklabels([])
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.fig.canvas.mpl_connect(
            "button_press_event",
            lambda x: print(self.layout.pixel2hex((x.xdata, x.ydata)).round()),
        )

    def plot_hex(
        self, he, fill=False, fillcolor=None, edgecolor=None, alpha=1
    ):
        """Renders hexagon"""
        patch = Polygon(
            self.layout.hex_corners(he),
            fill=fill,
            facecolor=fillcolor,
            edgecolor=edgecolor,
            alpha=alpha,
        )
        self.ax.add_patch(patch)

    def plot_hexmap(self, hm, colors, ignore_func=lambda x: False):
        """Renders collection of hexagons"""
        cmap = LinearSegmentedColormap.from_list("terrain", colors)

        patches = []
        for he, val in hm.items():
            if ignore_func(he):
                continue
            patch = Polygon(self.layout.hex_corners(he), color=cmap(val))
            patches.append(patch)
        pc = PatchCollection(patches, match_original=True)
        self.ax.add_collection(pc)

    def plot_path(self, path, width=1, color=None):
        """Renders a trace connecting given hexagons"""
        if not path or len(path) < 2:
            return
        xy = np.array([self.layout.hex2pixel(he) for he in path])
        self.ax.plot(xy[:, 0], xy[:, 1], linewidth=width, color=color)

    def plot_edge(self, he, di, width=1, color=None):
        """Renders hexagon's edge in given direction"""
        edge = self.layout.hex_edge(he, di)
        self.ax.plot(edge[:, 0], edge[:, 1], color=color, linewidth=width)

    def plot_border(self, edges, width=1, color=None):
        if len(edges) == 0:
            return
        xy = np.array([self.layout.hex_edge(e) for e in edges])
        xy = xy.reshape(-1, xy.shape[-1])
        xy = np.delete(xy, np.arange(1, xy.shape[0] - 1, 2), axis=0)
        self.ax.plot(xy[:, 0], xy[:, 1], linewidth=width, color=color)

    def label(self, he, text, color=None):
        """Renders text inside hexagon"""
        pos = self.layout.hex2pixel(he)
        self.ax.annotate(
            text, pos, ha="center", va="center", color=color
        )

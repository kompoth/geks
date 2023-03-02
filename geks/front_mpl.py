"""
A simple frontend based on matplotlib written for debug purposes.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


class FrontMPL:
    """A class that encapsulates matplotlib frontend."""
    def __init__(self, layout):
        """Constructor."""
        self.layout = layout
        self.fig, self.ax = plt.subplots(1)
        self.ax.set_aspect('equal')

        cid = self.fig.canvas.mpl_connect(
            'button_press_event',
            lambda x: print(self.layout.pixel2hex(
                (x.xdata, x.ydata)
            ).round())
        )

    def show(self):    
        """Shows rendered objects with selected matplotlib backend."""
        plt.gca().invert_yaxis()
        plt.autoscale(enable = True)
        plt.show()
        
    def plot_hex(
        self, he, fill=False, fillcolor=None, edgecolor=None, alpha=1
    ):
        """Renders hexagon."""
        patch = Polygon(
            self.layout.hex_corners(he), 
            fill=fill,
            facecolor=fillcolor,
            edgecolor=edgecolor,
            alpha=alpha
        )
        self.ax.add_patch(patch)
    
    def plot_arrow(
        self, he1, he2, width=0.1, 
        fill=False, fillcolor=None, edgecolor=None
    ):
        """Renders an arrow pointing from hexagon 'he1' to 'he2'."""
        xy0 = self.layout.hex2pixel(he1)
        dxy = (self.layout.hex2pixel(he2) - xy0) * 0.2
        xy0 += dxy
        self.ax.arrow(
            xy0[0], xy0[1], 
            dxy[0], dxy[1],
            width=0.1, 
            fill=fill, facecolor=fillcolor, edgecolor=edgecolor
        ) 
    
    def plot_path(
        self, path, width=0.1, 
        fill=False, fillcolor=None, edgecolor=None
    ):
        """Renders a trace of arrows connecting given hexagons."""
        if not path or len(path) < 2:
            return
        he0 = path[0]
        for he in path[1:]:
            self.plot_arrow(
                he0, he, 
                fill=fill, fillcolor=fillcolor, edgecolor=edgecolor
            )
            he0 = he

    def label(self, he, text):
        """Renders text inside hexagon.""" 
        pos = self.layout.hex2pixel(he)
        lbl = self.ax.annotate(text, pos, ha="center", va="center")

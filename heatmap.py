import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

class Heatmap:
    def __init__(self,stimulus,pressed,size):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        scatter_p = ax.scatter(pressed[0], pressed[1], color='red', label='pressed', alpha=0)
        scatter_stim = ax.scatter(stimulus[0],stimulus[1], color='blue', marker='o', label='stimulus center', alpha=0)

        # add stimulus squares
        width = size
        height = size
        stim_coord = [stimulus[0], stimulus[1]]

        stim_zipped = zip(*stim_coord)
        for stim_x, stim_y in stim_zipped:
            ax.add_patch(
                Rectangle(xy=(stim_x - width / 2, stim_y - height / 2), width=width, height=height, linewidth=1,
                          color='blue', fill=False))
        ax.axis('equal')
        fig.legend((scatter_p, scatter_stim), ('Pressed', 'Stimulus Center'))
        fig.show()
        self.flat_pressedx = np.array(pressed[0]).ravel()
        self.flat_pressedy = np.array(pressed[1]).ravel()

    def heatmap(self,limitTrial):
        heatmap, xedges, yedges = np.histogram2d(self.flat_pressedx.ravel(), self.flat_pressedy.ravel(),
                                                 range=[[-500, 500], [-500, 500]], bins=limitTrial)

        return heatmap, xedges, yedges
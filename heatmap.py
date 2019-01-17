import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import time
import datetime

class scatterplot:
    def __init__(self,stimulus,pressed,size):
        self.startTime = self.timeStamp()

        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        self.scatter_p = ax.scatter(pressed[0], pressed[1], color='red', label='pressed', alpha=0, marker = 'x')
        self.scatter_stim = ax.scatter(stimulus[0],stimulus[1], color='blue', marker='o', label='stimulus center', alpha=0)

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

        self.flat_pressedx = np.array(pressed[0]).ravel()
        self.flat_pressedy = np.array(pressed[1]).ravel()

    def timeStamp(self):
        self.ts = time.time()
        self.st = datetime.datetime.fromtimestamp(self.ts).strftime('%Y-%m-%d')
        self.tt = datetime.datetime.fromtimestamp(self.ts).strftime('%H-%M-%S')
        return {'string': self.st, 'seconds': self.ts, 'time': self.tt}

    def heatmap_param(self,limitTrial):
        self.heatmap, self.xedges, self.yedges = np.histogram2d(self.flat_pressedx.ravel(), self.flat_pressedy.ravel(),
                                                 range=[[-600, 600], [-600, 600]], bins=limitTrial)
        return

    def saveheatmap(self,taskname,animal_ID,limitTrial):
        bounds = np.linspace(0,limitTrial,limitTrial+1)
        plt.imshow(self.heatmap.T, interpolation='bicubic', cmap=plt.cm.Reds,extent=[self.xedges[0], self.xedges[-1], self.yedges[0], self.yedges[-1]], origin='lower')
        plt.colorbar( norm='norm',ticks=bounds)
        plot_dir = r'./data' + "/" + str(animal_ID) + "/" + str(taskname) + "/"
        plt.savefig(plot_dir + self.st + self.tt + 'heatmap.png')
        return

    # def savescatterplot(self,taskname,animal_ID):
    #     self.fig.legend((self.scatter_p, self.scatter_stim), ('Pressed', 'Stimulus Center'))
    #     self.fig.show()
    #     plot_dir = r'./data'+ "/"+ str(animal_ID) + "/" + str(taskname) + "/"
    #     plt.savefig(plot_dir + 'time' + self.tt + 'scatter.png')
    #     return


class Finalized_Simulation_Animation:
    def __init__(self,figure,ax,animation):
        self.figure = figure
        self.ax = self.figure.add_subplot(xlim=(0, 2), ylim=(-1, 1))
        self.line, = self.ax.plot()
        self.animation = animation
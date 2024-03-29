import osmnx as ox
from matplotlib import pyplot as plt


class Map_Road_Choose:
    def __init__(self, G):
        self.fig = None
        self.ax = None
        self.G = G
        self.scatter_src = None
        self.scatter_dst = None
        self.is_temp = False
        self.edge = None
        self.src = None
        self.dst = None


    def onclick(self, event):
        if event.xdata is not None and event.ydata is not None:
            # Get the limits of the plot

            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

            # Transform the clicked point to lon, lat
            x, y = event.xdata, event.ydata
            # Find the nearest node (junction) to the clicked point
            self.edge = ox.distance.nearest_edges(self.G, x, y) # returns a tuple of (u, v, key)
            self.src = self.G.nodes[self.edge[0]]
            self.dst = self.G.nodes[self.edge[1]]


            if self.is_temp is True:
                self.scatter_src.remove()
                self.scatter_dst.remove()
            self.scatter_src = self.ax.scatter(self.src['x'], self.src['y'], color='green', s=50, label=f'start point (node id: {self.edge[0]})')
            self.scatter_dst = self.ax.scatter(self.dst['x'], self.dst['y'], color='red', s=50, label=f'end point (node id: {self.edge[1]})')
            self.is_temp = True


            plt.legend()
            self.fig.canvas.draw()
            print("Clicked road OSMID:", self.edge)

    def create_show_map(self):

        self.fig, self.ax = ox.plot_graph(self.G, bgcolor='white', node_color='black', show=False, close=False)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.text(0.01, 0.01, "Choose a road to block by clicking on it. "
                                  "\n Click on the arrows below to move the map")
        plt.show()

    def get_road(self):
        return self.edge

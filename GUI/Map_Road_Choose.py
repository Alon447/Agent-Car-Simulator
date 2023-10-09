import osmnx as ox
from matplotlib import pyplot as plt


class Map_Road_Choose:
    def __init__(self, G, controller=None):
        self.fig = None
        self.ax = None
        self.road_id = None
        self.G = G
        self.mouse_pressed = False
        self.key_pressed = False
        self.curr_x = None
        self.curr_y = None
        self.count = 0
        self.scatter_src = None
        self.scatter_dst = None
        self.controller = controller
        self.is_temp = False
        self.have_src = False
        self.have_dst = False
        self.cur_gdf = None

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
            # self.cur_gdf = gpd.GeoDataFrame(geometry=[Point(lon, lat)],crs='epsg:4326')
            # self.cur_gdf.plot(ax=self.ax, color='black', label='clicked point')

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

    # def onpress(self, event):
    #     if event.key is None:
    #         return
    #     try:
    #         if event.key in ['a', 'z', 'r', 'q']:
    #             self.scatter.remove()
    #         if event.key == 'a':
    #             self.key_pressed = True
    #             print("pressed a")
    #             self.create_src()
    #         elif event.key == 'z':
    #             self.key_pressed = True
    #             print("pressed z")
    #             self.create_dst()
    #         elif event.key == 'r':
    #             self.key_pressed = True
    #             print("pressed r")
    #             self.reset_src_dst()
    #     except:
    #         pass
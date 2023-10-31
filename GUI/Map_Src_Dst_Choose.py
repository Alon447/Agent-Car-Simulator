import matplotlib.pyplot as plt
import osmnx as ox
import geopandas as gpd
import Utilities.Getters as Getters
from shapely.geometry import Point




class Map_Src_Dst_Choose:
    def __init__(self, G, controller=None):
        self.fig = None
        self.ax = None
        self.src_osmid = None
        self.dst_osmid = None
        self.G = G
        self.mouse_pressed = False #
        self.key_pressed = False
        self.curr_x = None
        self.curr_y = None
        self.count = 0 #
        self.scatter = None
        self.src_scatter = None #
        self.dst_scatter = None #
        self.controller = controller
        self.is_temp = False
        self.have_src = False #
        self.have_dst = False #
        self.cur_gdf = None

    def onclick(self, event):
        if event.xdata is not None and event.ydata is not None:

            # Transform the clicked point to lon, lat
            x, y = event.xdata, event.ydata
            # Find the nearest node (junction) to the clicked point
            self.osmid = ox.distance.nearest_nodes(self.G, x, y)

            self.curr_x = self.G.nodes[self.osmid]['x']
            self.curr_y = self.G.nodes[self.osmid]['y']

            if self.is_temp is True:
                self.scatter.remove()
                # self.cur_gdf.remove()
            fixed_osmid = self.controller.get_fixed_node_id(self.osmid)
            self.scatter = self.ax.scatter(self.curr_x, self.curr_y, color='gray', s=50, label=f'temporary (node id: {fixed_osmid})')
            self.is_temp = True

            plt.legend()
            self.fig.canvas.draw()
            print("Clicked Junction OSMID:", self.osmid)

    def onpress(self, event):
        if event.key is None:
            return
        try:
            if event.key in ['a', 'z', 'r']:
                if self.is_temp is True:
                    self.scatter.remove()
            if event.key == 'a':
                self.key_pressed = True
                print("pressed a")
                self.create_src()

            elif event.key == 'z':
                self.key_pressed = True
                print("pressed z")
                self.create_dst()

            elif event.key == 'r':
                self.key_pressed = True
                print("pressed r")
                self.reset_src_dst(True)

        except Exception as e:
            print("Error in onpress")
            print(e)


    def create_src(self):
        if self.src_scatter is not None:
            self.src_scatter.remove()
        self.is_temp = False
        self.src_scatter = self.ax.scatter(self.curr_x, self.curr_y, color='green', s=50, label='Start')
        self.src_osmid = self.osmid
        # self.have_src = True
        plt.legend()
        self.fig.canvas.draw()

    def create_dst(self):
        if self.dst_scatter is not None:
            self.dst_scatter.remove()
        self.is_temp = False
        self.dst_scatter = self.ax.scatter(self.curr_x, self.curr_y, color='red', s=50, label='End')
        self.dst_osmid = self.osmid
        # self.have_dst = True
        plt.legend()
        self.fig.canvas.draw()

    def reset_src_dst(self,is_pressed_r=False):

        self.scatter = None
        self.is_temp = False
        self.scatter = None
        self.curr_x = None
        self.curr_y = None
        self.src_osmid = None
        self.dst_osmid = None
        if self.src_scatter is not None:
            self.src_scatter.remove()
            self.src_scatter = None
            # self.fig.canvas.draw()
        if self.dst_scatter is not None:
            self.dst_scatter.remove()
            self.dst_scatter = None
            # self.fig.canvas.draw()

        if is_pressed_r is True:
            plt.legend()
            self.fig.canvas.draw()

    def create_show_map(self):

        self.fig, self.ax = ox.plot_graph(self.G, bgcolor='white', node_color='black', show=False, close=False)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('key_press_event', self.onpress)
        self.fig.text(0.01, 0.01, "Press 'a' to choose source, 'z' to choose destination, 'r' to reset, 'q' to quit "
                                  "\n also, click on the arrows below to move the map")
        plt.show()

    def get_nodes_id(self):
        return self.src_osmid, self.dst_osmid

    def clear(self):
        # self.fig.clear()

        # self.ax.clear()
        self.osmid = None
        self.mouse_pressed = False
        self.curr_x = None
        self.curr_y = None
        self.prev_x = None
        self.prev_y = None

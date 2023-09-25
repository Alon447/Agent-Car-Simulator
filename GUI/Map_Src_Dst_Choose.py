import matplotlib.pyplot as plt
import osmnx as ox

import Utilities.Getters as Getters


# TODO: maybe change it so it will immidiateley show the changes on the map
#   also maybe add somewhere else explaination for the functionality: a - src, z - dst, r - reset, q - quit

class Map_Src_Dst_Choose:
    def __init__(self, G, controller=None):
        self.fig = None
        self.ax = None
        self.src_osmid = None
        self.dst_osmid = None
        self.G = G
        self.mouse_pressed = False
        self.key_pressed = False
        self.curr_x = None
        self.curr_y = None
        self.count = 0
        self.scatter = None
        self.src_scatter = None
        self.dst_scatter = None
        self.controller = controller
        self.is_temp = False
        self.have_src = False
        self.have_dst = False

    def onclick(self, event):
        if event.xdata is not None and event.ydata is not None:
            # Get the limits of the plot

            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

            # Transform the clicked point to lon, lat
            lat, lon = event.xdata, event.ydata
            # Find the nearest node (junction) to the clicked point
            self.osmid = ox.distance.nearest_nodes(self.G, lat, lon)

            self.curr_x = self.G.nodes[self.osmid]['x']
            self.curr_y = self.G.nodes[self.osmid]['y']

            if self.is_temp is True:
                self.scatter.remove()
            fixed_osmid = self.controller.get_node_id_from_osm_id(self.osmid)
            self.scatter = self.ax.scatter(self.curr_x, self.curr_y, color='gray', s=50, label=f'temporary (node id: {fixed_osmid})')
            self.is_temp = True
            plt.legend()

            print("Clicked Junction OSMID:", self.osmid)

    def onpress(self, event):
        if event.key is None:
            return
        try:
            if event.key in ['a', 'z', 'r', 'q']:
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
                self.reset_src_dst()
            elif event.key == 'q':
                print("pressed q")
                plt.close()
        except:
            pass

    def create_src(self):
        if self.src_scatter is not None:
            self.src_scatter.remove()
        self.is_temp = False
        self.src_scatter = self.ax.scatter(self.curr_x, self.curr_y, color='green', s=50, label='Start')
        self.src_osmid = self.osmid
        # self.have_src = True
        plt.legend()

    def create_dst(self):
        if self.dst_scatter is not None:
            self.dst_scatter.remove()
        self.is_temp = False
        self.dst_scatter = self.ax.scatter(self.curr_x, self.curr_y, color='red', s=50, label='End')
        self.dst_osmid = self.osmid
        # self.have_dst = True
        plt.legend()

    def reset_src_dst(self):

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
        if self.dst_scatter is not None:
            self.dst_scatter.remove()
            self.dst_scatter = None

    def create_show_map(self):

        self.fig, self.ax = ox.plot_graph(self.G, bgcolor='white', node_color='black', show=False, close=False)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('key_press_event', self.onpress)
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
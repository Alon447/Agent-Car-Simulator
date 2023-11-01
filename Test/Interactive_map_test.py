import matplotlib.pyplot as plt
import osmnx as ox

import Utilities.Getters as Getters


class MapClickHandler:
    def __init__(self, fig=None, ax=None, G=None):
        self.fig = fig
        self.ax = ax
        self.src_osmid = None
        self.dst_osmid = None
        self.G = G
        self.mouse_pressed = False
        self.key_pressed = False
        self.curr_x = None
        self.curr_y = None
        self.count = 0
        self.scatter = None

    def onclick(self, event):
        if event.xdata is not None and event.ydata is not None:
            # Get the limits of the plot
            # ax.clear()
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

            # Transform the clicked point to lon, lat
            lat, lon = event.xdata, event.ydata
            # Find the nearest node (junction) to the clicked point
            self.osmid = ox.distance.nearest_nodes(self.G, lat, lon)

            self.curr_x = self.G.nodes[self.osmid]['x']
            self.curr_y = self.G.nodes[self.osmid]['y']

            # if self.scatter is not None and self.count == 2:
            #     self.scatter.remove(self.curr_x, self.curr_y)
            #     self.count = 0
            if self.scatter is not None and self.scatter.get_label() == 'temporary':
                self.scatter.remove()
            self.scatter = self.ax.scatter(self.curr_x, self.curr_y, color='gray', s=50, label='temporary')
            # plt.legend()
            print("Clicked Junction OSMID:", self.osmid)
            # fig.canvas.draw()
            # fig.canvas.flush_events()
            self.count += 1

    def onpress(self, event):
        if event.key == 'a':
            self.key_pressed = True
            self.create_src()
            print("pressed a")
        elif event.key == 'z':
            self.key_pressed = True
            self.create_dst()
            print("pressed z")
        elif event.key == 'r':
            self.key_pressed = True
            self.reset_src_dst()
            print("pressed r")
        elif event.key == 'q':
            plt.close()

    def create_src(self):
        self.scatter = self.ax.scatter(self.curr_x, self.curr_y, color='green', s=50, label='Start')
        plt.legend()

    def create_dst(self):
        self.scatter = self.ax.scatter(self.curr_x, self.curr_y, color='red', s=50, label='End')
        plt.legend()

    def reset_src_dst(self):
        self.scatter.remove()
        self.scatter = None
        self.curr_x = None
        self.curr_y = None
        # self.count = 0

    def create_show_map(self):
        location = (40.7128, -74.0060)  # New York City
        network_type = "drive"

        # G = ox.graph_from_point(location, dist=1000, network_type=network_type)
        self.G, _ = Getters.get_graph('TLV')
        self.fig, self.ax = ox.plot_graph(self.G, bgcolor='white', node_color='black', show=False, close=False)
        click_handler = MapClickHandler(self.fig, self.ax, self.G)
        self.fig.canvas.mpl_connect('button_press_event', click_handler.onclick)
        self.fig.canvas.mpl_connect('key_press_event', click_handler.onpress)
        plt.show()

    def get_nodes_id(self):
        return self.src_osmid,self.dst_osmid

    def clear(self):
        # self.fig.clear()
        self.ax.clear()
        self.osmid = None
        self.mouse_pressed = False
        self.curr_x = None
        self.curr_y = None
        self.prev_x = None
        self.prev_y = None


# Example usage
if __name__ == "__main__":
    temp_map = MapClickHandler(None, None, None)
    temp_map.create_show_map()
    print("done")


import matplotlib.pyplot as plt
import osmnx as ox
import geopandas as gpd
import Utilities.Getters as Getters
from shapely.geometry import Point
import traceback

# TODO: maybe change it so it will immidiateley show the changes on the map
#   also maybe add somewhere else explaination for the functionality: a - src, z - dst, r - reset, q - quit
SOURCE = 'src'
DESTINATION = 'dst'
TEMPORARY = 'temp'
SOURCE_COLOR = 'green'
DESTINATION_COLOR = 'red'
SOURCE_AND_DESTINATION = 'src_dst'
SOURCE_AND_DESTINATION_COLOR = 'yellow'
TEMPORARY_COLOR = 'blue'
MARKERS_TYPES_LIST = [SOURCE, DESTINATION, TEMPORARY, SOURCE_AND_DESTINATION]


class Map_Src_Dst_Choose:
    def __init__(self, G, controller=None):
        self.fig = None
        self.ax = None
        self.src_osmid = None
        self.dst_osmid = None
        self.G = G
        self.mouse_pressed = False  #
        self.key_pressed = False
        self.curr_x = None
        self.curr_y = None
        self.count = 0  #
        # self.scatter = None
        self.src_scatter = None  #
        self.dst_scatter = None  #
        self.controller = controller
        self.is_temp = False
        self.cur_gdf = None
        self.mark_hover = False
        self.markers_dicts = {}
        for type in MARKERS_TYPES_LIST:
            self.markers_dicts[type] = {}

    def onclick(self, event):
        if event.xdata is not None and event.ydata is not None:

            # Transform the clicked point to lon, lat
            x, y = event.xdata, event.ydata
            # Find the nearest node (junction) to the clicked point
            self.osmid = ox.distance.nearest_nodes(self.G, x, y)

            self.curr_x = self.G.nodes[self.osmid]['x']
            self.curr_y = self.G.nodes[self.osmid]['y']

            if self.is_temp is True:
                keys_to_iterate = list(self.markers_dicts[TEMPORARY].keys())
                for point in keys_to_iterate:
                    self.markers_dicts[TEMPORARY][point].remove()
                    del self.markers_dicts[TEMPORARY][point]
                # self.cur_gdf.remove()
            # fixed_osmid = self.controller.get_fixed_node_id(self.osmid)
            self.markers_dicts[TEMPORARY][self.osmid] = self.ax.scatter(self.curr_x, self.curr_y, color='blue', s=50)
            self.is_temp = True

            plt.legend()
            self.fig.canvas.draw()
            print("Clicked Junction OSMID:", self.osmid)

    def onpress(self, event):
        if event.key is None or event.key == 'q' or event.key not in ['a', 'z', 'r', 'm', 'u', 'x']:
            return
        try:
            # if event.key in ['a', 'z', 'r','m','u','x']:
            if event.key == 'a':
                self.key_pressed = True
                print("pressed a")
                if self.mark_hover is True:
                    self.mark_hover = False
                self.create_src_dst(SOURCE_COLOR, SOURCE, DESTINATION)

            elif event.key == 'z':
                self.key_pressed = True
                print("pressed z")
                if self.mark_hover is True:
                    self.mark_hover = False
                self.create_src_dst(DESTINATION_COLOR, DESTINATION, SOURCE)

            elif event.key == 'r':
                self.key_pressed = True
                print("pressed r")
                self.reset_src_dst(True)

            elif event.key == 'm':
                self.key_pressed = True
                print("pressed m")
                self.mark_hover = not self.mark_hover

            elif event.key == 'u':
                self.key_pressed = True
                print("pressed u")
                if self.mark_hover is True:
                    self.mark_hover = False
                self.remove_singular_marker(self.osmid)

            elif event.key == 'x':
                self.key_pressed = True
                print("pressed x")
                if self.mark_hover is True:
                    self.mark_hover = False
                self.remove_multiple_markers()

                return

        except Exception as e:
            print("Error in onpress")
            print(e)
            # print error traceback
            traceback.print_exc()

    def create_src_dst(self, color, type, opposite_type):
        for point in self.markers_dicts[TEMPORARY].keys():
            if point in self.markers_dicts[type].keys():
                self.markers_dicts[TEMPORARY][point].set_color(color)
                continue
            elif point in self.markers_dicts[opposite_type].keys():
                self.markers_dicts[opposite_type][point].remove()
                del self.markers_dicts[opposite_type][point]
                self.markers_dicts[SOURCE_AND_DESTINATION][point] = self.markers_dicts[TEMPORARY][point]
                self.markers_dicts[SOURCE_AND_DESTINATION][point].set_color(SOURCE_AND_DESTINATION_COLOR)
            else:
                self.markers_dicts[TEMPORARY][point].set_color(color)
                self.markers_dicts[type][point] = self.markers_dicts[TEMPORARY][point]
        self.markers_dicts[TEMPORARY] = {}
        # plt.legend()
        self.fig.canvas.draw()

    def remove_singular_marker(self, osmid):
        for dict in self.markers_dicts.values():
            if osmid in dict.keys():
                dict[osmid].remove()
                del dict[osmid]
        # plt.legend()
        self.fig.canvas.draw()

    def remove_multiple_markers(self):
        keys_to_remove = list(self.markers_dicts[TEMPORARY].keys())
        for dict in self.markers_dicts.values():
            cur_dict_keys = list(dict.keys())
            for point in keys_to_remove:
                if point in cur_dict_keys:
                    dict[point].remove()
                    del dict[point]
        # self.markers_dicts[TEMPORARY] = {}
        # plt.legend()
        self.fig.canvas.draw()

    def on_hover(self, event):  # when M is pressed, hovering over a graph will mark nearby nodes blue
        if event.xdata is not None and event.ydata is not None and self.mark_hover is True:
            # Transform the clicked point to lon, lat
            x, y = event.xdata, event.ydata
            # Find the nearest node (junction) to the clicked point
            self.osmid = ox.distance.nearest_nodes(self.G, x, y)
            self.curr_x = self.G.nodes[self.osmid]['x']
            self.curr_y = self.G.nodes[self.osmid]['y']
            # self.curr_x, self.curr_y = x, y
            # if self.is_temp is True:
            #     self.scatter.remove()
            #     self.cur_gdf.remove()
            # fixed_osmid = self.controller.get_fixed_node_id(self.osmid)
            if self.osmid in self.markers_dicts[TEMPORARY].keys():
                return
            self.markers_dicts[TEMPORARY][self.osmid] = self.ax.scatter(self.curr_x, self.curr_y, color='blue', s=50)
            self.is_temp = True

            # plt.legend()
            self.fig.canvas.draw()
            print("Hovering over Junction OSMID:", self.osmid)

    def reset_src_dst(self, is_pressed_r=False):
        self.is_temp = False
        self.curr_x = None
        self.curr_y = None
        self.reset_scatter_dicts()

        if is_pressed_r is True:
            # plt.legend()
            self.fig.canvas.draw()

    def reset_scatter_dicts(self):
        for scatter_dict in self.markers_dicts.values():
            cur_scatter_dict_keys = list(scatter_dict.keys())
            for scatter in cur_scatter_dict_keys:
                scatter_dict[scatter].remove()
                del scatter_dict[scatter]

    def create_show_map(self, sources=None, destinations=None):
        # TODO: maybe plot existing source and destination
        self.fig, self.ax = ox.plot_graph(self.G, bgcolor='white', node_color='black', show=False, close=False)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('key_press_event', self.onpress)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_hover)
        self.fig.text(0.01, 0.01,
                      f'after left clicking or marking by pressing \'m\' and hovering: Press \'a\' to choose \n '
                      'source, \'z\' to choose destination,\'u\' after clicking to unmark a point \n or \'x\' afer '
                      'hovering to unmark multiple points. \'r\' to reset, \'q\' to quit.\n'
                      f'{TEMPORARY_COLOR} points are temporary, {SOURCE_COLOR} are source, {DESTINATION_COLOR} are destination, {SOURCE_AND_DESTINATION_COLOR} are both.'
                      "\n also, click on the arrows below to move the map")
        plt.show()

    def get_sources_and_destinations(self):
        all_sources = list(self.markers_dicts[SOURCE].keys()) + list(self.markers_dicts[SOURCE_AND_DESTINATION].keys())
        all_destinations = list(self.markers_dicts[DESTINATION].keys()) + list(
            self.markers_dicts[SOURCE_AND_DESTINATION].keys())
        return all_sources, all_destinations

    def clear(self):
        # self.fig.clear()

        # self.ax.clear()
        self.osmid = None
        self.mouse_pressed = False
        self.curr_x = None
        self.curr_y = None
        self.prev_x = None
        self.prev_y = None


if __name__ == "__main__":
    G, _ = Getters.get_graph("TLV")
    m = Map_Src_Dst_Choose(G)
    m.create_show_map()
    src, dst = m.get_nodes_id()
    print(src, dst)
    print("done")

import osmnx as ox
import matplotlib.pyplot as plt
import sklearn
import Utilities.Getters as Getters

class MapClickHandler:
    def __init__(self, fig, ax,G):
        self.fig = fig
        self.ax = ax
        self.osmid = None
        self.G = G

    def onclick(self, event):
        if event.xdata is not None and event.ydata is not None:
            # Get the limits of the plot
            # ax.clear()
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

            # Transform the clicked point to lon, lat
            lat, lon = event.xdata, event.ydata
            ax.scatter(lat, lon, color='green', s=50, label='Start')
            # Find the nearest node (junction) to the clicked point
            self.osmid = ox.distance.nearest_nodes(G,lat, lon)
            print("Clicked Junction OSMID:", self.osmid)
            # fig.canvas.draw()
            # fig.canvas.flush_events()

# Example usage
if __name__ == "__main__":
    # Replace this with your desired location and network type
    location = (40.7128, -74.0060)  # New York City
    network_type = "drive"


    # G = ox.graph_from_point(location, dist=1000, network_type=network_type)
    G,_ = Getters.get_graph('TLV')
    fig, ax = ox.plot_graph(G, show=False, close=False)
    click_handler = MapClickHandler(fig, ax,G)
    fig.canvas.mpl_connect('button_press_event', click_handler.onclick)
    plt.show()

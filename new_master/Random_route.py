from random import random

import Route


class Random_route(Route):

        def get_next_road(self, source_road, destination_node, time):
            # TODO: update according to connectivity list implementation
            optional_roads = connectivity_list[source_road]
            return random.choice(optional_roads)

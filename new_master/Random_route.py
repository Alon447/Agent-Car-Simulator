from random import random

import Route


class Random_route(Route):

        def get_next_road(self, source_road, destination_node, time):
            """
            :param source_road: Road
            :param destination_node:
            :param time: 0 for now
            :return:  next road to travel to : Road
            """
            # TODO: update according to connectivity list implementation
            optional_roads = source_road.get_adjacent_roads() # list of IDs of optional roads

            return random.choice(optional_roads)

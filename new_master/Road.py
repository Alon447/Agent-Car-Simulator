
class Road:
    def __init__(self, id , source_node, destination_node, length, max_speed, street_count, traffic_lights):
        self.id= id
        self.source_node = int(source_node)
        self.destination_node = int(destination_node)
        self.length = length
        self.current_speed = 10
        self.max_speed = max_speed
        self.is_blocked= False
        self.cars_on_road = []
        self.adjacent_roads = [] # list of adjacent roads to this road, includes only the ids of the roads

        # new attributes,
        self.street_count= street_count # represents the number of intersections this road has
        self.traffic_lights = traffic_lights # represents if this road has traffic lights

    # Gets
    def get_id(self):
        return self.id
    def get_source_node(self):
        return self.source_node
    def get_destination_node(self):
        return self.destination_node
    def get_length(self):
        return self.length
    def get_current_speed(self):
        return self.current_speed
    def get_max_speed(self):
        return self.max_speed
    def get_is_blocked(self):
        return self.is_blocked
    def get_cars_on_road(self):
        return self.cars_on_road
    def get_adjacent_roads(self):
        return self.adjacent_roads

    def get_street_count(self):
        return self.street_count
    def get_traffic_lights(self):
        return self.traffic_lights
    # Sets
    def set_current_speed(self, speed):
        self.current_speed = speed
    def set_adjacent_roads(self, adjacent_roads):
        self.adjacent_roads = adjacent_roads
    # Functions
    def block(self):
        self.is_blocked = True
    def unblock(self):
        self.is_blocked = False
    def add_car_to_road(self, car):
        self.cars_on_road.append(car)
    def remove_car_from_road(self, car):
        self.cars_on_road.remove(car)
    def update_speed(self, new_speed):
        self.current_speed = new_speed
    def calculate_time(self):
        """
        Calculates the time it takes to travel on this road
        length - meters
        speed - km/h
        time - seconds
        so we need to convert speed to m/s by dividing by 3.6
        :return:
        """

        if self.current_speed == None:
            print("error")
        total_time = 3.6 * self.length/self.current_speed
        if self.traffic_lights:
            total_time += 30#60
        return round(total_time,2)

    def __str__(self):
        return "Road id: " + str(self.id) + ", source node: " + str(self.source_node) + ", destination node: " + str(self.destination_node) + ", length: " + str(self.length) + ", max speed: " + str(self.max_speed) + ", current speed: " + str(self.current_speed) + ", is blocked: " + str(self.is_blocked) #+ ", cars on road: " + str(self.cars_on_road)

    def __repr__(self):
        return f"Road(road_id={self.id}, source_node={self.source_node}, destination_node={self.destination_node}, length={self.length}, speed={self.current_speed})"

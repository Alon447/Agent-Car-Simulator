
class Road:
    def __init__(self, id ,source_node ,destination_node ,length,max_speed):
        self.id= id
        self.source_node = source_node
        self.destination_node = destination_node
        self.length = length
        self.current_speed = 0
        self.max_speed = max_speed
        self.is_blocked= False
        self.cars_on_road = []
        self.adjacent_roads = [] # list of adjacent roads to this road, includes only the ids of the roads

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
        return self.length/self.current_speed

    def __str__(self):
        return "Road id: " + str(self.id) + " source node: " + str(self.source_node) + " destination node: " + str(self.destination_node) + " length: " + str(self.length) + " max speed: " + str(self.max_speed) + " current speed: " + str(self.current_speed) + " is blocked: " + str(self.is_blocked) + " cars on road: " + str(self.cars_on_road)

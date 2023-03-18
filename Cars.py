


class Cars:
    def __init__(self, id, route,next_node_index):
        self.id = id
        self.route = route
        self.nextNode = route[0]

    def get_id(self):
        return self.id

    def get_route(self):
        return self.route

    def get_next_node_index(self):
        return self.next_node_index

    def set_next_node_index(self, next_node_index):
        self.next_node_index = next_node_index

    def set_route(self, route):
        self.route = route

    def move_node(self):
        self.next_node_index += 1
    def __str__(self):
        return "id: " + self.id + "\n" + "route: " + str(self.route) + "\n" + "next node: " + str(self.route[self.next_node_index])
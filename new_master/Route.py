from abc import abstractmethod, ABC


class Route(ABC):
    @abstractmethod
    def get_next_road(self, source_road, destination_node, time):
        pass
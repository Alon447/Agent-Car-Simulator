import datetime

from Main_Files.Road_Network import Road_Network
class Q_Agent:
    def __init__(self, src: int, dst: int, start_time: datetime, road_network: Road_Network):
        self.src = src
        self.dst = dst
        self.start_time = start_time
        self.road_network = road_network
        self.current_road = None
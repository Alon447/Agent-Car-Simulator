import Car
from new_master import Road_Network


class CarManager :

    """
    Purpose: this class will manage all the cars in the simulation.
    It will be used to add cars to the simulation, remove cars from the simulation, and update the cars.
    It will also be used to keep track of the next time a car will update,  in order to update the simulation time accordingly.
    When a car ends its journey, it will be removed from the simulation, and it's information will be saved for statistics.

    CONTAINS:

    cars_in_simulation - dict of all the cars currently in the simulation
    cars_finished - list of all the cars that finished their journey
    cars_nearest_update - list that will contain car id and time of the next update, the list will always be sorted by time.
                          when car updates we will remove it from the list, update its time and will be inserted by binary search.

    """
    def __init__(self):
        self.cars_in_simulation = {}        # a dictionary of all the cars currently in the simulation.

        self.cars_nearest_update = []       # a list of the cars that will determine time of the next update.
        self.cars_nearest_update_time = 0   # the time of the next update
        self.cars_finished = []  # a list of the cars that have finished their journey and are waiting to be removed from the simulation
        self.cars_stuck = []                # a list of the cars that are stuck in the simulation


    """
    cars_in_simulation=[1:[1, 0,100, 20],3:[3, 3,20, 30]]
    
    getters
    """
    def get_cars_in_simulation(self):
        return self.cars_in_simulation

    def get_cars_finished(self):
        return self.cars_finished

    """
    setters and updaters
    """

    def add_car(self, car):
        car.start_car()
        self.cars_in_simulation[car.get_id()] = car
        self.sort_cars_in_simulation()
        #self.add_to_time_queue(car)
        #self.sort_cars_in_simulation()
        #self.calc_nearest_update_time()

    def remove_car(self, car):
        self.cars_in_simulation.remove(car)
        self.cars_finished.append(car)
        self.calc_nearest_update_time()


    """
    calculation functions
    """


    def sort_cars_in_simulation(self):
        # sort the dict by the time until the next road
        # also update the nearest update time
        if(len(self.cars_in_simulation) == 0):
            self.cars_nearest_update_time=0
            return False
        self.cars_in_simulation = dict(sorted(self.get_cars_in_simulation().items(), key=lambda item: item[1].get_time_until_next_road()))
        first_index, first_car = next(iter(self.cars_in_simulation.items()))
        self.cars_nearest_update_time = first_car.get_time_until_next_road()

    def calc_nearest_update_time(self):
        self.cars_nearest_update_time = self.cars_in_simulation[0].get_time_until_next_road()
        for car in self.cars_in_simulation:
            if car.get_time_until_next_road() < self.cars_nearest_update_time:
                self.cars_nearest_update_time = car.get_time_until_next_road()


    def show_cars_in_simulation(self):
        print("cars_in_simulation:")
        print(self.cars_in_simulation)

    def update_cars(self, time):
        """
        this function will update all the cars in the simulation.
        it will be called by the simulation class.
        we need to update the time of the nearest update time.
        update for every car the time until the next road.
        and change the road for the cars that finished their road.

        :param time:
        :return:
        """
        cars = self.cars_in_simulation.copy()
        for keys in self.cars_in_simulation:
            car = cars[keys]
            car.update_travel_time(time)
            if car.get_time_until_next_road() == 0:
                if car.move_next_road()==None:
                    cars.pop(car.get_id())
                    if car.get_car_in_destination():
                        print("car", car.get_id(), "finished his journey")
                        self.cars_finished.append(car)
                    else:
                        print("car", car.get_id(), "is stuck")
                        self.add_stuck_car(car)
        self.cars_in_simulation = cars
        self.sort_cars_in_simulation()
        return

    def get_nearest_update_time(self):
        return self.cars_nearest_update_time

    def get_cars_stuck(self):
        return self.cars_stuck

    def add_stuck_car(self, car):
        self.cars_stuck.append(car)

    def is_car_stuck(self, car):
        return car in self.cars_stuck
    def is_car_finished(self, car):
        return car in self.cars_finished

    def clear(self):
        self.cars_in_simulation.clear()
        self.cars_finished.clear()
        self.cars_stuck.clear()
        self.cars_nearest_update_time = 0






import datetime

import Car
from Main_Files import Road_Network


class CarManager:
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
        # Start of the simulation
        self.cars_waiting_to_enter = []  # a list of the cars that are waiting to enter the simulation, i.e their starting time has not arrived yet.

        # During the simulation
        self.cars_in_simulation = {}  # a dictionary of all the cars currently in the simulation.
        self.cars_nearest_update = []  # a list of the cars that will determine time of the next update.
        self.cars_nearest_update_time = 0  # the time of the next update
        self.cars_blocked = []  # a list of the cars that are blocked in the simulation

        # End of the simulation
        self.cars_finished = []  # a list of the cars that have finished their journey and are waiting to be removed from the simulation
        self.cars_stuck = []  # a list of the cars that are stuck at the end of the simulation
        self.updated_dictionary = {}  # a dictionary of the cars that have been updated in the current time
        # step. key is time, value is a list of the cars that have been updated in that time step
        # along with current node


    """
    setters and updaters
    """

    def add_update_to_dictionary(self, time, car_id, x,y, node_id):
        if time not in self.updated_dictionary:
            self.updated_dictionary[time] = []
        self.updated_dictionary[time].append((car_id, (x,y), node_id))

    def add_car(self, car, time):
        car_starting_time = car.starting_time
        if car_starting_time > time:  # car is not ready to enter the simulation
            self.cars_waiting_to_enter.append(car)
            self.cars_waiting_to_enter.sort(key=lambda x: x.starting_time)

        else:  # car is ready to enter the simulation
            car.start_car()
            self.cars_in_simulation[car.id] = car
        self.sort_cars_in_simulation()
        self.calc_nearest_update_time(time)
        x, y = car.get_xy_source()
        self.add_update_to_dictionary(car_starting_time, car.id, x, y, car.source_node)

    """
    calculation functions
    """

    def sort_cars_in_simulation(self):
        # sort the dict by the time until the next road
        # also update the nearest update time
        if len(self.cars_in_simulation) == 0:
            # self.cars_nearest_update_time=0
            return False
        self.cars_in_simulation = dict(
            sorted(self.cars_in_simulation.items(), key=lambda item: item[1].get_time_until_next_road()))
        first_index, first_car = next(iter(self.cars_in_simulation.items()))
        self.cars_nearest_update_time = first_car.get_time_until_next_road()

    def calc_nearest_update_time(self, time: datetime.datetime):
        """
        this function will calculate the time of the nearest update.
        :return:
        """
        if self.cars_waiting_to_enter:
            date_time = self.cars_waiting_to_enter[0].starting_time  # datetime object
            time1 = int((date_time - time).total_seconds())  # timedelta object
        else:
            time1 = float('inf')

        if self.cars_in_simulation:
            first_index, first_car = next(iter(self.cars_in_simulation.items()))
            time2 = first_car.get_time_until_next_road()  # int object
        else:
            time2 = float('inf')
        self.cars_nearest_update_time = min(time1, time2)
        return self.cars_nearest_update_time

    def find_earliest_waiting_car(self):
        """
        this function will return the earliest time that a car is waiting to enter the simulation.
        :return:
        """
        if not self.cars_waiting_to_enter:
            return None
        starting_time = self.cars_waiting_to_enter[0].starting_time
        for car in self.cars_waiting_to_enter:
            if car.starting_time < starting_time:
                starting_time = car.starting_time
        return starting_time

    # def show_cars_in_simulation(self):
    #     print("cars_in_simulation:")
    #     print(self.cars_in_simulation)

    def update_cars(self, timeStamp: int, current_datetime: datetime.datetime):
        """
        this function will update all the cars in the simulation.
        it will be called by the simulation class.
        we need to update the time of the nearest update time.
        update for every car the time until the next road.
        and change the road for the cars that finished their road.

        :param timeStamp:
        :return:
        """
        cars = self.cars_in_simulation.copy()
        blocked_cars = self.cars_blocked.copy()
        for key in self.cars_in_simulation:
            moved = True
            car = cars[key]
            car.update_travel_time(timeStamp)

            if car.get_time_until_next_road() == 0:
                result = car.move_next_road(timeStamp)  # result is the next road the car is on
                x, y = car.get_xy_current()
                self.add_update_to_dictionary(current_datetime, car.id, x, y, car.current_road.source_node[0])
                # add update to list
                if result is None:  # car is finished or stuck
                    cars.pop(car.id)
                    moved = False

                    if car.car_in_destination:
                        print("car", car.id, "finished his journey")
                        self.cars_finished.append(car)
                        x, y = car.get_xy_destination()
                        self.add_update_to_dictionary(current_datetime, car.id, x, y, car.destination_node)
                    else:
                        print("car", car.id, "is stuck")
                        self.cars_stuck.append(car)

                elif result == "blocked":  # car is blocked
                    print("car", car.id, "is blocked in road ", car.current_road.id)
                    self.cars_blocked.append(car)
                    car.is_blocked = True
                    blocked_cars.append(car)
                    moved = False
            if moved == True and car.is_blocked:
                car.is_blocked = False
                blocked_cars.remove(car)  # TODO: check if needed
                cars[key] = car
                moved = False

        # after we updated all the cars, we need to handle the waiting cars
        copy_waiting_cars = self.cars_waiting_to_enter.copy()
        for car in copy_waiting_cars:
            if car.starting_time <= current_datetime:
                car.start_car()
                cars[car.id] = car
                self.cars_waiting_to_enter.remove(car)
            else:
                break

        self.cars_in_simulation = cars
        self.cars_blocked = blocked_cars
        self.sort_cars_in_simulation()
        return

    def is_car_stuck(self, car):
        return car in self.cars_stuck

    def is_car_finished(self, car):
        return car in self.cars_finished

    def clear(self):
        self.cars_in_simulation.clear()
        self.cars_finished.clear()
        self.cars_stuck.clear()
        self.cars_nearest_update_time = 0
        for car in self.cars_blocked:
            car.is_blocked = False
        self.cars_blocked.clear()

    def get_all_cars_ids(self):
        return list(self.cars_in_simulation.keys()) + [car.id for car in self.cars_blocked]
    # def force_cars_to_finish(self):
    #     for car in self.cars_stuck:
    #         car.force_finish()
            # self.cars_finished.append(car)

    """
       cars_in_simulation=[1:[1, 0,100, 20],3:[3, 3,20, 30]]

       GET
    """

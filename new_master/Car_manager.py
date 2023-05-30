import Car

class CarManager :

    """
    Purpose: this class will manage all the cars in the simulation.
    It will be used to add cars to the simulation, remove cars from the simulation, and update the cars.
    It will also be used to keep track of the next time a car will update,  in order to update the simulation time accordingly.
    When a car ends its journey, it will be removed from the simulation, and it's information will be saved for statistics.

    CONTAINS:

    cars_in_simulation - list of all the cars currently in the simulation
    cars_finished - list of all the cars that finished their journey
    cars_nearest_update - list that will contain car id and time of the next update, the list will always be sorted by time.
                          when car updates we will remove it from the list, update its time and will be inserted by binary search.

    """
    def __init__(self):
        self.cars_in_simulation = {}        # a dictionary of all the cars currently in the simulation.
        self.cars_finished = []             # a list of the cars that have finished their journey and are waiting to be removed from the simulation
        self.cars_nearest_update = []       # a list of the cars that will determine time of the next update. might not be needed.
        self.cars_nearest_update_time = 0   # the time of the next update


    """
    cars_in_simulation=[1:[1, 0,100, 20],3:[3, 3,20, 30]
    
    
    getters
    """
    def get_cars_in_simulation(self):
        return self.cars_in_simulation

    def get_cars_finished(self):
        return self.cars_finished

    def get_cars_nearest_update(self):
        return self.cars_nearest_update

    def get_cars_nearest_update_time(self):
        return self.cars_nearest_update_time



    """
    setters and updaters
    """

    def add_car(self, car):
        self.cars_in_simulation[car.get_id()] = car
        #self.calc_nearest_update_time()

    def remove_car(self, car):
        self.cars_in_simulation.remove(car)
        self.cars_finished.append(car)
        self.calc_nearest_update_time()


    """
    calculation functions
    """
    def calc_nearest_update_time(self):
        self.cars_nearest_update_time = self.cars_in_simulation[0].get_time_until_next_road()
        for car in self.cars_in_simulation:
            if car.get_time_until_next_road() < self.cars_nearest_update_time:
                self.cars_nearest_update_time = car.get_time_until_next_road()

    def calc_nearest_update_cars(self):
        self.cars_nearest_update = []
        for car in self.cars_in_simulation:
            if car.get_time_until_next_road() == self.cars_nearest_update_time:
                self.cars_nearest_update.append(car)

cm = CarManager()
car1=Car.Car(1,0,10,0)
car3=Car.Car(3,1,8,0)
car20=Car.Car(20,2,9,0)
cm.add_car(car1)
cm.add_car(car20)
cm.add_car(car3)
print(cm.get_cars_in_simulation()[car20.get_id()])
print("bye")

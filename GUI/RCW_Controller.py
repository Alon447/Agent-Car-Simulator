# external imports
import datetime

# internal imports
from GUI import Map_Multi_Src_Dst_Choose as mmsdc
from Utilities import Errors as errors
from Utilities.Getters import *



class RCW_Controller:
    """
    This class is used to control the route comparison window
    """
    def __init__(self, view, controller):

        self.use_existing_q_tables = None
        self.add_traffic_white_noise = None
        self.traffic_lights = None
        self.rain_intensity = None
        self.destinations = None
        self.sources = None
        self.view = view
        self.controller = controller
        self.cars_amount = 0
        self.simulations_amount = 0
        self.earliest_timedate_pick = None
        self.latest_timedate_pick = None
        self.used_algorithms = {}  # key: algorithm name, value: boolean
        self.mmsdc = None

    def start_route_comparison(self):
        self.controller.set_multiple_runs_parameters(self.cars_amount, self.simulations_amount, self.used_algorithms,
                                                     self.sources, self.destinations, self.rain_intensity,
                                                     self.traffic_lights,
                                                     self.add_traffic_white_noise, self.use_existing_q_tables, self.earliest_timedate_pick,
                                                     self.latest_timedate_pick)
        self.controller.prepare_routing_comparisons()
    def prepare_route_comparison(self):
        # parameters:
        #   cars amount
        #   simulation amount
        #   routing algorithms
        #   graph
        #   sources and destinations
        #   starting time and date
        #   simulation duration (in seconds) (time untill the end date and time plus 2 hours)
        #   rain intensity
        #   traffic lights
        #   add traffic white noise
        #   use existing q tables
        #   number of episodes
        #   max steps per episode

        self.get_all_parameters()
        ready_to_start_comparisons = self.check_all_parameters()
        if ready_to_start_comparisons:
            self.start_route_comparison()

        pass

    def get_fixed_timedate_format(self, title_key):
        year, month, day, hour, minute, second = self.view.get_time_date(title_key)
        return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    def get_all_parameters(self):
        self.cars_amount = self.view.get_cars_amount()
        self.simulations_amount = self.view.get_simulations_amount()
        self.used_algorithms = self.view.get_used_algorithms()
        self.sources, self.destinations = self.mmsdc.get_sources_and_destinations()
        self.rain_intensity = self.view.get_rain_intensity()
        self.traffic_lights = self.view.get_traffic_lights()
        self.add_traffic_white_noise = self.view.get_add_traffic_white_noise()
        self.use_existing_q_tables = self.view.get_use_existing_q_tables()
        self.earliest_timedate_pick = self.get_fixed_timedate_format(Start_key)
        self.latest_timedate_pick = self.get_fixed_timedate_format(End_key)

    def check_all_parameters(self):
        all_checks_passed = True

        all_checks_passed &= self.check_cars_amount()
        all_checks_passed &= self.check_simulations_amount()
        all_checks_passed &= self.check_cars_and_sims_amount()
        all_checks_passed &= self.check_used_algorithms()
        all_checks_passed &= self.check_sources_and_destinations()
        all_checks_passed &= self.check_starting_time()
        return all_checks_passed


    def toggle_algorithm(self, algorithm, algorithm_var):
        self.used_algorithms[algorithm] = algorithm_var.get()

    def load_city_map(self):
        city_name = self.view.get_city_name()
        is_map_loaded = self.controller.load_city_map(city_name)
        if is_map_loaded:
            print("loaded city map")
            self.view.set_load_status_label("City map loaded")
            self.map_loaded = True
        else:
            print("failed to load city map")
            self.view.set_load_status_label("Failed to load city map")
            self.map_loaded = False

    def choose_src_dst(self):
        """
        This function is used to choose the source and destination of the car
        :return:
        """
        G, self.G_name = self.controller.get_graph()
        if self.G_name is None:
            errors.no_map_loaded_error()
        if self.mmsdc is None:
            self.mmsdc = mmsdc.Map_Src_Dst_Choose(G, self.controller)
            self.mmsdc.reset_src_dst()
        self.mmsdc.create_show_map()


    def back_to_main_menu(self):
        # Destroy the current simulation window if it exists
        self.view.destroy()

        # Unhide the main window
        # self.view.deiconify()
        self.controller.start_main_window()

    def check_cars_amount(self):
        passed_check = True
        if not self.cars_amount.isdigit():
            passed_check = False
        elif int(self.cars_amount) <= 0:
            passed_check = False
        if not passed_check:
            errors.incorrect_input_in_number_field_error('cars amount')
            return False
        self.cars_amount = int(self.cars_amount)
        return passed_check

    def check_simulations_amount(self):
        passed_check = True
        if not self.simulations_amount.isdigit():
            passed_check = False
        elif int(self.simulations_amount) <= 0:
            passed_check = False
        if not passed_check:
            errors.incorrect_input_in_number_field_error('simulations amount')
            return False
        self.simulations_amount = int(self.simulations_amount)
        return passed_check

    def check_cars_and_sims_amount(self):
        if self.cars_amount * self.simulations_amount < 2:
            errors.not_enough_routes_error()
            return False
        return True

    def check_used_algorithms(self):
        if len(self.used_algorithms) == 0:
            errors.no_algorithms_to_compare_error()
            return False
        return True

    def check_sources_and_destinations(self):
        if len(self.sources) == 0:
            errors.no_source_selected_error()
            return False
        if len(self.destinations) == 0:
            errors.no_destination_selected_error()
            return False
        return True


    def check_starting_time(self):
        if self.earliest_timedate_pick >= self.latest_timedate_pick:
            errors.starting_time_error()
            return False
        return True

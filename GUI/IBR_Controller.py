import datetime

import GUI.Map_Road_Choose as mrc
class IBR_Controller:
    def __init__(self, view, view_master, controller):
        self.view = view
        self.controller = controller
        self.G_name = None
        self.mrc = None
        self.road_values = {}


    def choose_road(self):
        G, self.G_name = self.controller.get_graph()
        if self.G_name is None:
            self.view.no_map_loaded_error()
        if self.mrc is None:
            self.mrc = mrc.Map_Road_Choose(G, self.controller)
        self.mrc.create_show_map()
        print("chosen road:", self.mrc.get_road())

        return

    def confirm_choice(self):
        # get the starting time
        day, month, year = self.view.get_start_date()
        hour = self.view.get_start_hour()
        minute = self.view.get_start_minute()
        second = self.view.get_start_second()
        starting_time = datetime.datetime(year = year, month = month, day = day, hour = hour, minute = minute,
                                          second = second)
        # get the ending time
        day, month, year = self.view.get_end_date()
        hour = self.view.get_end_hour()
        minute = self.view.get_end_minute()
        second = self.view.get_end_second()
        ending_time = datetime.datetime(year = year, month = month, day = day, hour = hour, minute = minute,
                                          second = second)
        try:
            edge = self.mrc.get_road()
            if edge is None:
                self.view.no_road_selected_error()
            fixed_id = self.controller.get_fixed_road_id(edge[0], edge[1])
            fixed_src = self.controller.get_fixed_node_id(edge[0])
            fixed_dst = self.controller.get_fixed_node_id(edge[1])
            print("chosen road id:", fixed_id)
            print("chosen source:", fixed_src)
            print("chosen destination:", fixed_dst)
            print("chosen starting time:", starting_time)
            print("chosen ending time:", ending_time)

            road_to_add = (fixed_id, fixed_src, fixed_dst, starting_time, ending_time)
            self.view.add_road(road = road_to_add)
            self.road_values[fixed_id] = road_to_add
            self.controller.add_blockage_values(road_to_add, fixed_id, starting_time, ending_time)
            # self.controller.add_car_values(car_to_add,
            #                                self.cur_car_id)  # maybe add cars only when simulation is about to start  # self.controller.add_car_init(starting_time, src, dst, routing_algorithm,  #                              self.view.get_use_existing_q_tables())

        except Exception as e:
            self.view.general_error()
            print(e)

    def load_existing_blockages(self):
        # cur_car_values_dict = self.controller.get_cars_values_dict()
        # for id in cur_car_values_dict.keys():
        #     self.cur_car_id = max(self.cur_car_id, cur_car_values_dict[id][0])
        #     self.cars_vaules[id] = cur_car_values_dict[id]
        #     self.view.add_car(cur_car_values_dict[id])
        pass
    def delete_blockage(self, selected):
        if type(selected) is tuple:
            for item in selected:
                item_id, item_start_time, item_end_time = self.view.road_id_from_treeview(item)
                del self.road_values[item_id]
                self.treeview_delete_blockage(item)
                self.controller.remove_blockage_values(item_id)
        else:
            del self.road_values[selected]
            self.treeview_delete_blockage(selected)

    def treeview_delete_blockage(self,selected):
        tree = self.view.get_existing_blockages_treeview()
        if type(selected) is tuple:
            for item in selected:
                tree.delete(item)
        else:
            tree.delete(selected)
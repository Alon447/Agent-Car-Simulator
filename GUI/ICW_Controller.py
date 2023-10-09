import datetime

from GUI import Map_Src_Dst_Choose as msdc


# TODO: add functions to send the car parameters to the controller
class ICW_Controller:
    def __init__(self, view, view_master, controller):
        # self.choose_date = None
        self.view = view
        self.controller = controller
        self.G_name = None
        self.msdc = None
        self.cars_values = {}
        self.cur_car_id = 0


    def confirm_choice(self):
        # needed car parameters:
        #   starting time
        #   source
        #   destination
        #   road network (from simulation manager)
        #   car id (from simulation manager or auto generated)
        #   routing algorithm (+if using existing Q table)
        # TODO: change relevant parameters to the ones chosen by the user
        day, month, year = self.view.get_date()
        hour = self.view.get_hour()
        minute = self.view.get_minute()
        second = self.view.get_second()
        starting_time = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        try:
            src, dst = self.msdc.get_nodes_id()
            if src is None:
                self.view.no_source_selected_error()
            if dst is None:
                self.view.no_destination_selected_error()
            routing_algorithm = self.view.get_routing_algorithm()
            print("chosen src and dst:", src, dst)
            print("chosen starting time:", starting_time)
            print("chosen routing algorithm:", self.view.get_routing_algorithm())
            print("chosen date: ", self.view.get_raw_date())
            print("use existing q table: ", self.view.get_use_existing_q_tables())
            # self.view.destroy()
            self.cur_car_id += 1
            fixed_src = self.controller.get_fixed_node_id(src)
            fixed_dst = self.controller.get_fixed_node_id(dst)

            car_to_add = (self.cur_car_id,fixed_src,fixed_dst,starting_time, routing_algorithm,
                                         self.view.get_use_existing_q_tables())
            self.cars_values[self.cur_car_id] = car_to_add
            self.view.add_car(car_to_add)
            self.controller.add_car_values(car_to_add, self.cur_car_id)
            #maybe add cars only when simulation is about to start
            # self.controller.add_car_init(starting_time, src, dst, routing_algorithm,
            #                              self.view.get_use_existing_q_tables())

        except Exception as e:
            if self.msdc is None:
                self.view.no_source_selected_error()
            else:
                self.view.general_error()
            print(e)



    def load_existing_cars(self):
        cur_car_values_dict = self.controller.get_cars_values_dict()
        for id in cur_car_values_dict.keys():
            self.cur_car_id = max(self.cur_car_id, cur_car_values_dict[id][0])
            self.cars_values[id] = cur_car_values_dict[id]
            self.view.add_car(cur_car_values_dict[id])

    def choose_src_dst(self):
        G, self.G_name = self.controller.get_graph()
        if self.G_name is None:
            self.view.no_map_loaded_error()
        if self.msdc is None:
            self.msdc = msdc.Map_Src_Dst_Choose(G, self.controller)
        self.msdc.reset_src_dst()
        self.msdc.create_show_map()
        print("chosen src and dst:", self.msdc.get_nodes_id())

    # def choose_date(self):
    #     pass
    #
    # def toggle_use_existing_tables(self):
    #     pass

    def delete_cars(self,selected):
        if type(selected) is tuple:
            for item in selected:
                item_id = self.view.car_id_from_treeview(item)
                del self.cars_values[item_id]
                self.treeview_delete_cars(item)
                self.controller.remove_car_values(item_id)
        else:
            del self.cars_values[selected]
            self.treeview_delete_cars(selected)

    def treeview_delete_cars(self,selected):
        tree = self.view.get_existing_cars_treeview()
        if type(selected) is tuple:
            for item in selected:
                tree.delete(item)
        else:
            tree.delete(selected)
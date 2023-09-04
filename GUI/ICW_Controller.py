import datetime

from GUI import Map_Src_Dst_Choose as msdc

#TODO: add functions to send the car parameters to the controller
class ICW_Controller:
    def __init__(self,view,view_master,controller):
        self.view = view
        self.controller = controller
        self.G_name = None
        self.msdc = None

    def confirm_choice(self):
        #needed car parameters:
        #   starting time
        #   source
        #   destination
        #   road network (from simulation manager)
        #   car id (from simulation manager or auto generated)
        #   routing algorithm (+if using existing Q table)
        #TODO: change relevant parameters to the ones chosen by the user
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        hour = self.view.get_hour()
        minute = self.view.get_minute()
        second = self.view.get_second()
        starting_time = datetime.datetime(year = year, month = month, day = day, hour = hour, minute = minute, second = second)
        try:
            src,dst = self.msdc.get_nodes_id()
            if src is None:
                self.view.no_source_selected_error()
            if dst is None:
                self.view.no_destination_selected_error()
        except:
            if self.msdc is None:
                self.view.no_source_selected_error()

        pass

    def choose_src_dst(self):
        G,self.G_name = self.controller.get_graph()
        if self.G_name is None:
            self.view.no_map_loaded_error()
        if self.msdc is None:

            self.msdc = msdc.Map_Src_Dst_Choose(G,self.controller)
        self.msdc.reset_src_dst()
        self.msdc.create_show_map()
        print("chosen src and dst:" , self.msdc.get_nodes_id())

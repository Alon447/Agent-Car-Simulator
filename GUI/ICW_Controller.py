from GUI import Map_Src_Dst_Choose as msdc

#TODO: add functions to send the car parameters to the controller
class ICW_Controller:
    def __init__(self,view,view_master,controller):
        self.view = view
        self.controller = controller
        self.G_name = None
        self.msdc = None

    def confirm_choice(self):
        pass

    def choose_src_dst(self):
        G,self.G_name = self.controller.get_graph()
        if self.G_name is None:
            self.view.no_map_loaded_error()
        if self.msdc is None:
            self.msdc = msdc.Map_Src_Dst_Choose(G,self.controller)
        self.msdc.create_show_map()
        print("chosen src and dst:" , self.msdc.get_nodes_id())

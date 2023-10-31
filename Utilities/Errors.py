import tkinter as tk

"""
This file contains all the error messages that are used in the program
"""


def cant_run_simulation_error():
    tk.messagebox.showerror("Error", "Can't run simulation, please check that all parameters are set correctly")
def no_map_loaded_error():
    tk.messagebox.showerror("Error", "No map loaded!")

def no_source_selected_error():
    tk.messagebox.showerror("Error", "No source selected!")

def no_destination_selected_error():
    tk.messagebox.showerror("Error", "No destination selected!")

def general_error():
    tk.messagebox.showerror("Error", "Something went wrong!")

def no_road_selected_error():
    tk.messagebox.showerror("Error", "No road selected!")

def already_blocked_error():
    tk.messagebox.showerror("Error", "Road already blocked!")

def no_roads_to_remove_error():
    tk.messagebox.showerror("Error", "No roads to remove!")

def add_cars_error():
    tk.messagebox.showerror("Error", "Please add cars before starting the simulation")

def no_path_between_src_dst_error():
    tk.messagebox.showerror("Error", "No Path Found!")
def src_equal_dst_error():
    tk.messagebox.showerror("Error", "Source and Destination are the same!")

def incorrect_input_in_number_field_error(field_name):
    tk.messagebox.showerror("Error", f'Incorrect input in  field: {field_name}. \n Please enter a valid number')

def no_algorithms_to_compare_error():
    tk.messagebox.showerror("Error", "Please choose at least one algorithm to compare")

def starting_time_error():
    tk.messagebox.showerror("Error", "Please enter a valid starting time (later than ending time")


def no_file_chosen_error():
    tk.messagebox.showerror("Error", "Please choose a file to load")
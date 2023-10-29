import datetime
import tkinter as tk
from tkinter import ttk, Scrollbar
from tkcalendar import Calendar, DateEntry
import GUI.DCRW_Controller as dcrwc
from Utilities.Getters import *


class Display_Comparisons_Results_Window(tk.Tk):

    def __init__(self, controller):
        row = 0
        super().__init__()
        self.controller = controller
        self.title("Display Comparisons Results")
        self.dcrwc = dcrwc.DCRW_Controller(self, controller)

        # show numerical statistics: standard deviation, average
        # self.show_numerical_statistics_button = ttk.Button(self, text="Show numerical statistics",
        #                                                   command=self.dcrc.show_numerical_statistics)
        # textbox for statistics
        self.statistics_textbox = tk.Text(self, height=10, width=50)
        self.statistics_textbox.grid(row=row, column=0, padx=10, pady=10)

        # display past results files in treeview
        row += 1
        self.past_car_times_results_treeview = ttk.Treeview(self, column=("c1"),
                                                            show='headings', height=10, selectmode="browse")
        self.past_car_times_results_treeview.column("#1", width=200, anchor=tk.CENTER)
        self.past_car_times_results_treeview.heading("#1", text="Name")
        self.past_car_times_results_treeview.grid(row=row, column=0, padx=50, pady=50)
        self.dcrwc.load_past_results()

        # confirm button
        row += 1
        self.confirm_button = ttk.Button(self, text="Confirm Cars Times File",
                                         command=lambda: self.dcrwc.confirm(
                                             self.past_car_times_results_treeview.selection(),
                                             self.past_car_times_results_treeview))
        self.confirm_button.grid(row=row, column=0, padx=10, pady=10)
        # back to menu button
        row += 1
        self.back_button = ttk.Button(self, text="Back To Main Menu", command=self.dcrwc.back_to_menu)

    def set_textbox_statistics(self, statistics_dict):
        self.statistics_textbox.delete("1.0", "end")
        self.statistics_textbox.insert(tk.END, "Statistics:\n")
        for algorithm in statistics_dict:
            self.statistics_textbox.insert(tk.END, algorithm + ":\n")
            for key in statistics_dict[algorithm]:
                self.statistics_textbox.insert(tk.END, key + ": " + str(statistics_dict[algorithm][key]) + "\n")
        self.statistics_textbox.configure(state='disabled')

    def add_existing_car_times_files(self, car_times_files):
        for file in car_times_files:
            self.past_car_times_results_treeview.insert("", tk.END, values=(file,))

    def main(self):
        self.mainloop()

    def simulation_id_from_treeview(self, simulation_id, treeview):
        return treeview.item(simulation_id)['values'][0]

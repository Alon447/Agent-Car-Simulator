# external imports
import tkinter as tk
from tkinter import ttk

# internal imports
import GUI.DCRW_Controller as dcrwc
from Utilities.Getters import *

class Display_Comparisons_Results_Window(tk.Tk):

    def __init__(self, controller):
        row = 0
        super().__init__()
        self.controller = controller
        self.title("Display Comparisons Results")
        self.dcrwc = dcrwc.DCRW_Controller(self, controller)

        # textbox for statistics
        self.statistics_textboxes = {}
        col = 0
        for variable in Variables_for_statistics:
            self.statistics_textboxes[variable] = tk.Text(self, height=10, width=50)
            self.statistics_textboxes[variable].grid(row=row, column=col, padx=10, pady=10)
            col += 1

        # display past results files in treeview
        row += 1
        self.results_variables_treeviews = {}
        col = 0
        for variable in Variables_for_statistics:
            self.results_variables_treeviews[variable] = ttk.Treeview(self, column=("c1"),
                                                                      show='headings', height=10, selectmode="browse")
            self.results_variables_treeviews[variable].column("#1", width=200, anchor=tk.CENTER)
            self.results_variables_treeviews[variable].heading("#1", text=variable)
            self.results_variables_treeviews[variable].grid(row=row, column=col, padx=50, pady=50)
            col += 1
        self.dcrwc.load_past_results()

        # confirm button
        row += 1
        self.confirm_buttons = {}
        col = 0
        for variable in Variables_for_statistics:
            self.confirm_buttons[variable] = ttk.Button(self, text="Confirm " + variable + " File",
                                                        command=lambda v = variable: self.dcrwc.confirm(
                                                            self.results_variables_treeviews[v].selection(),
                                                            self.results_variables_treeviews[v],v))
            self.confirm_buttons[variable].grid(row=row, column=col, padx=10, pady=10)
            col += 1

        # back to menu button
        row += 1
        self.back_button = ttk.Button(self, text="Back To Main Menu", command=self.dcrwc.back_to_menu)
        self.back_button.grid(row=row, column=0, padx=10, pady=10)

    def set_textbox_statistics(self, statistics_dict, variable):
        self.statistics_textboxes[variable].configure(state='normal')
        self.statistics_textboxes[variable].delete("1.0", "end")
        self.statistics_textboxes[variable].insert(tk.END, "Driving Time Statistics:\n")
        for algorithm in statistics_dict:
            self.statistics_textboxes[variable].insert(tk.END, algorithm + ":\n")
            for key in statistics_dict[algorithm]:
                self.statistics_textboxes[variable].insert(tk.END, key + ": " + str(statistics_dict[algorithm][key]) + "\n")
        self.statistics_textboxes[variable].configure(state='disabled')

    def add_existing_times_files(self, times_files, variable_for_statistics):
        for file in times_files:
            self.results_variables_treeviews[variable_for_statistics].insert("", tk.END, values=(file,))



    def simulation_id_from_treeview(self, simulation_id, treeview):
        return treeview.item(simulation_id)['values'][0]

    def main(self):
        self.mainloop()
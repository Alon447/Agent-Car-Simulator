import datetime
import tkinter as tk
from tkinter import ttk, Scrollbar
from tkcalendar import Calendar, DateEntry
import GUI.DCR_Controller as dcrc
from Utilities.Getters import *

class Display_Comparisons_Results(tk.Tk):

    def __init__(self,controller):
        row = 0
        super().__init__()
        self.controller = controller
        self.title("Display Comparisons Results")
        self.dcrc = dcrc.DCR_Controller(self, controller)

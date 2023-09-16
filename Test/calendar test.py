# # Import Required Library
# from tkinter import *
# from tkcalendar import Calendar
#
# # Create Object
# root = Tk()
#
# # Set geometry
# root.geometry("400x400")
#
# # Add Calendar
# cal = Calendar(root, selectmode='day',
#                year=2020, month=5,
#                day=22)
#
# cal.pack(pady=20)
#
#
# def grad_date():
#     date.config(text="Selected Date is: " + cal.get_date())
#
#
# # Add Button and Label
# Button(root, text="Get Date",
#        command=grad_date).pack(pady=20)
#
# date = Label(root, text="")
# date.pack(pady=20)
#
# # Execute Tkinter
# root.mainloop()


# Import the required libraries
# from tkinter import *
# from tkinter import ttk
#
# def delete(selected):
#     if type(selected) is tuple:
#         for item_ind in selected:
#             print("delete: ", tree.item(item_ind))
#             tree.delete(item_ind)
#     else:
#         tree.delete(selected)
#
# def print_children(tree):
#     for item in tree.get_children():
#         print("item: ", tree.item(item))
#
# # Create an instance of tkinter frame
# win = Tk()
#
# # Set the size of the tkinter window
# win.geometry("700x350")
#
# s = ttk.Style()
# s.theme_use('clam')
#
# # Add a Treeview widget
# tree = ttk.Treeview(win, column=("c1", "c4", "c3"), show='headings', height=5, selectmode="extended")
#
# tree.column("# 1", anchor=CENTER)
# tree.heading("# 1", text="ID")
# tree.column("# 2", anchor=CENTER)
# tree.heading("# 2", text="FName")
# tree.column("# 3", anchor=CENTER)
# tree.heading("# 3", text="LName")
#
# # Insert the data in Treeview widget
# tree.insert('', 'end', values=('1', 'Joe', 'Nash'))
# tree.insert('', 'end', values=('2', 'Emily', 'Mackmohan'))
# tree.insert('', 'end', values=('3', 'Estilla', 'Roffe'))
# tree.insert('', 'end', values=('4', 'Percy', 'Andrews'))
# tree.insert('', 'end', values=('5', 'Stephan', 'Heyward'))
#
# tree.pack()
#
# delete_button = ttk.Button(win, text="Delete", command=lambda: delete(tree.selection()))
# delete_button.pack()
#
# print_tree_button = ttk.Button(win, text="Print Tree", command=lambda :print_children(tree))
# print_tree_button.pack()
#
# win.mainloop()
# Python program to illustrate the usage of
# treeview scrollbars using tkinter


from tkinter import ttk
import tkinter as tk

# Creating tkinter window
window = tk.Tk()
window.resizable(width = 1, height = 1)

# Using treeview widget
treev = ttk.Treeview(window, selectmode ='browse')

# Calling pack method w.r.to treeview
treev.pack(side ='right')

# Constructing vertical scrollbar
# with treeview
verscrlbar = ttk.Scrollbar(window,
						orient ="vertical",
						command = treev.yview)

# Calling pack method w.r.to vertical
# scrollbar
verscrlbar.pack(side ='right', fill ='x')

# Configuring treeview
treev.configure(xscrollcommand = verscrlbar.set)

# Defining number of columns
treev["columns"] = ("1", "2", "3")

# Defining heading
treev['show'] = 'headings'

# Assigning the width and anchor to the
# respective columns
treev.column("1", width = 90, anchor ='c')
treev.column("2", width = 90, anchor ='se')
treev.column("3", width = 90, anchor ='se')

# Assigning the heading names to the
# respective columns
treev.heading("1", text ="Name")
treev.heading("2", text ="Sex")
treev.heading("3", text ="Age")

# Inserting the items and their features to the
# columns built
treev.insert("", 'end', text ="L1",
			values =("Nidhi", "F", "25"))
treev.insert("", 'end', text ="L2",
			values =("Nisha", "F", "23"))
treev.insert("", 'end', text ="L3",
			values =("Preeti", "F", "27"))
treev.insert("", 'end', text ="L4",
			values =("Rahul", "M", "20"))
treev.insert("", 'end', text ="L5",
			values =("Sonu", "F", "18"))
treev.insert("", 'end', text ="L6",
			values =("Rohit", "M", "19"))
treev.insert("", 'end', text ="L7",
			values =("Geeta", "F", "25"))
treev.insert("", 'end', text ="L8",
			values =("Ankit", "M", "22"))
treev.insert("", 'end', text ="L10",
			values =("Mukul", "F", "25"))
treev.insert("", 'end', text ="L11",
			values =("Mohit", "M", "16"))
treev.insert("", 'end', text ="L12",
			values =("Vivek", "M", "22"))
treev.insert("", 'end', text ="L13",
			values =("Suman", "F", "30"))

# Calling mainloop
window.mainloop()


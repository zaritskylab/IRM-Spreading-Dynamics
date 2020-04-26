import tkinter as tk
import numpy as np
import warnings
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfilename
from tkinter import messagebox, Checkbutton
from Procedures import Procedures as procudures
# the apps tkinter main Style attribute
LARGE_FONT = ("Verdana", 20)


class MainApplication(tk.Tk):
    """

    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Platelet Dynamics Quantification")
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = EntryPage(container, self)
        self.frames[EntryPage] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(EntryPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class EntryPage(tk.Frame):
    """
    the application "Home Page"
    """
    def __init__(self, parent, controller):
        self.procedures_module = procudures()
        tk.Frame.__init__(self, parent, bg="#211F1E")
        self.parent = parent
        self.controller = controller
        self.filename = ""
        self.param_kwargs = {
            "-time_scale": None, # int e.g. 5
            "-filter": None # str/bool e.g. 'True'/'False' or True/False
        }
        label = ttk.Label(self,
                          text="1. Upload a file. \n2.Select parameters (default ones are recommended)."
                               " \n3.Press start \n4. To run the example data, just press start")
        label.grid(row=0, column=0, columnspan=3)

        # parameters input
        label = ttk.Label(self,
                          text="Parameters [default recommended]:")

        label.grid(row=1, column=0, columnspan=3)
        # filter
        self.check_button_value_filter_param = IntVar(value=1)
        check_button = Checkbutton(self, text="Use smoothing filter", variable=self.check_button_value_filter_param)
        check_button.grid(row=2, column=0)
        # Frames per second input
        label = ttk.Label(self, text="Frames/second")
        label.grid(row=2, column=1)
        self.time_scale = StringVar(value="5")
        attach_threshold_entry = ttk.Entry(self, width=10, textvariable=self.time_scale)
        attach_threshold_entry.grid(row=2, column=2)

        # buttons
        button_upload_a_file = ttk.Button(self, text="Upload a file",
                                          command=self.file_dialog)
        button_upload_a_file.grid(row=3, column=1)

        button_to_start = ttk.Button(self, text="Start",
                                     command=self.start_quantifying)
        button_to_start.grid(row=3, column=0)

        button_to_show_help_dialog = ttk.Button(self, text="Help",
                                                command=self.show_help_dialog)
        button_to_show_help_dialog.grid(row=3, column=2)

    def show_help_dialog(self):
        help_text = ""
        with open('help.txt', 'r') as help_file:
            line = help_file.readline()
            while line is not None and line != "":
                help_text += line
                line = help_file.readline()
        messagebox.showinfo("Help:", help_text)

    def file_dialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select single platelet video",
                                                    filetypes=(("avi format", "*.avi"), ("all files", "*.*")))

    def start_quantifying(self):
        # getting the parameters:
        try:
            self.param_kwargs['-time_scale'] = int(self.time_scale.get())
        except Exception as e:
            self.param_kwargs['-time_scale'] = 5
            print(e)
        self.param_kwargs['-filter'] = bool(self.check_button_value_filter_param.get())
        messagebox.showinfo("Starting...", "now analyzing, please go to: \n['{0}/Results/']\n folder to see them".format(self.filename))
        if self.filename == "" or self.filename is None:
            # example run
            try:
                self.procedures_module.example_data_procedure(**self.param_kwargs)
            except Exception as e:
                messagebox.showinfo("Error!", "something went wrong, please try again or try our CLI.")
                print(e)
        else:
            try:
                self.procedures_module.new_data_procedure(self.filename, **self.param_kwargs)
            except Exception as e:
                messagebox.showinfo("Error!", "something went wrong, please try again or try our CLI.")
                print(e)


def start_gui():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        app = MainApplication()
        app.mainloop()
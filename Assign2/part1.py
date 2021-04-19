from tkinter import *
from ast import literal_eval
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Class for the right frame
class RightFrame(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.grid(row = 0, column = 1, sticky = NSEW)
        master.grid_rowconfigure(0, weight = 1)
        master.grid_columnconfigure(1, weight = 1)

    # Function to display the plot of the function using matplotlib
    def displayPlot(self, x_vals, y_vals):
        fig = plt.figure(figsize = (6, 5))
        plt.plot(x_vals, y_vals)
        plt.title("Plot of entered expression")
        plt.xlabel("Variable (x)")
        plt.ylabel("Value of expression (y)")
        canvas = FigureCanvasTkAgg(fig, master = self)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column = 0)
        toolbarFrame = Frame(master = self)
        toolbarFrame.grid(row = 2, column=0)
        toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)


# Class for the left frame
class LeftFrame(Frame):
    def __init__(self, master = None, rframe = None):
        Frame.__init__(self, master, bg = "cyan")
        self.master = master
        self.rframe = rframe
        self.grid(row = 0, column = 0, sticky = NSEW)
        master.grid_columnconfigure(0, weight = 1)
        master.grid_rowconfigure(0, weight = 1)

        self.lab_expr = Label(self, text = "Expression (variable x) : ")
        self.lab_expr.grid(row = 0, column = 0)

        self.expr_text = Text(self, width = 30, height = 3)
        self.expr_text.insert(END, "expr")
        self.expr_text.grid(row = 0, column = 1, columnspan = 2)

        self.lab_var = Label(self, text = "Variable Range (a, b) : ")
        self.lab_var.grid(row = 1, column = 0)

        self.var_text = Text(self, width = 30, height = 3)
        self.var_text.insert(END, "value")
        self.var_text.grid(row = 1, column = 1, columnspan = 2)

        self.eval_button = Button(self, text = "Evaluate", command = self.evaluate, width = 27, height = 2)
        self.eval_button.grid(row = 2, column = 0)

        self.exit_button = Button(self, text = "Exit", command = exit, width = 27, height = 2)
        self.exit_button.grid(row = 2, column = 1)

        self.values_text = Text(self, width = 60, height = 25)
        self.values_text.grid(row = 3, column = 0, columnspan = 2)

    # Function to display values taken by the function at few points
    def display_values(self, expr, x_vals, y_vals):
        self.values_text.delete(1.0, END)
        disp_str = ""
        num_points = len(x_vals)
        num_display = 20
        mul = num_points // num_display
        for i in range(num_display):
            disp_str = "At x = " + str(round(x_vals[i * mul], 4)) + ", y = " + str(round(y_vals[i * mul], 4)) + "\n"
            self.values_text.insert(END, disp_str)
        disp_str = "At x = " + str(x_vals[-1]) + ", y = " + str(y_vals[-1]) + "\n"
        self.values_text.insert(END, disp_str)

    # Function to evaluate the function at various points to plot it
    def evaluate(self):
        expr = self.expr_text.get(1.0, END)
        var_range = self.var_text.get(1.0, END)
        ab = literal_eval(var_range)
        num_points = 1000
        expr.strip("\n")
        x_vals = list()
        y_vals = list()
        for x in np.linspace(ab[0], ab[1], num_points):
            y = eval(expr)
            x_vals.append(x)
            y_vals.append(y)
        self.rframe.displayPlot(x_vals, y_vals)
        self.display_values(expr, x_vals, y_vals)


# Main window class
class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        master.geometry("1100x600")
        self.rightFrame = RightFrame(master)
        self.leftFrame = LeftFrame(master, self.rightFrame)
        master.wm_title("Expression Plotter")
        self.grid(row = 0, column = 0, sticky = NSEW)


# Basic tkinter root initialization
root  = Tk()
app = Window(root)
root.mainloop()
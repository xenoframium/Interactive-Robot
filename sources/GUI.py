from tkinter import *
from tkinter.ttk import *

UPDATE_INTERVAL = 10
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500


class GUI:
    def __init__(self, update_function):
        self.window = Tk()
        self.window.title("Robot")
        Style().theme_use('classic')
        self.canvas = Canvas(self.window, bg="white", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
        self.canvas.grid()

        self.update_function = update_function
        self.window.after(UPDATE_INTERVAL, self.__update)

    def mainloop(self):
        self.window.mainloop()

    def __update(self):
        self.update_function()
        self.window.after(UPDATE_INTERVAL, self.__update)

    def stop(self):
        self.window.destroy()
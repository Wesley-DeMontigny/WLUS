from GUI import *
import tkinter as tk
import os, signal
from struct import *


if __name__ == "__main__":
	DBServerStarup()

	root = tk.Tk()
	root.title("WLUS")
	app = Application(master=root)
	root.mainloop()

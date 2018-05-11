from GUI import *
import tkinter as tk


if __name__ == "__main__":
	DBServerStarup()

	root = tk.Tk()
	root.title("WLUS")
	app = Application(master=root)
	root.mainloop()

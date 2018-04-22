from threading import Thread, Timer
from bitstream import *
from reliability import PacketReliability
from replicamanager import *
from DBHandlers import *
from time import sleep
from GameMessage import *
from LDFReader import *
from __main__ import *
import sys
from World import WorldServer
from Auth import AuthServer
import tkinter as tk


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		master.protocol("WM_DELETE_WINDOW", self.on_closing)

		self.Auth = None
		self.World = None

		self.worldPane = None
		self.authPane = None

		self.menubar = tk.Menu(self.master)
		self.master.config(menu=self.menubar)
		self.create_widgets()
		self.pack()

		update = Thread(target=self.updateConsole)
		update.start()

	def serverLoop(self, loop):
		asyncio.set_event_loop(loop)
		loop.run_forever()

	def updateConsole(self):
		while True:
			if(self.Auth != None):
				if(self.Auth.updateConsole == True):
					self.Auth.updateConsole = False
					self.authPane.insert(tk.END, "[" + self.Auth.role + "]", "role")
					self.authPane.insert(tk.END, self.Auth.consoleMessage + "\n")
			if(self.World != None):
				if(self.World.updateConsole == True):
					self.World.updateConsole = False
					self.worldPane.insert(tk.END, "["+self.World.role+"]", "role")
					self.worldPane.insert(tk.END, self.World.consoleMessage + "\n")

	def runServer(self):
		self.World = WorldServer(("127.0.0.1", 2002), self, max_connections=10, incoming_password=b"3.25 ND1", role="WORLD")
		self.Auth = AuthServer(("127.0.0.1", 1001), self, max_connections=10, incoming_password=b"3.25 ND1", role="AUTH")

		loop = asyncio.get_event_loop()
		t = Thread(target=self.serverLoop, args=(loop,))
		t.start()

		self.menubar.entryconfig("Start Server", state="disabled")


	def create_widgets(self):
		#Create menu items
		self.menubar.add_command(label="Start Server", command=self.runServer)

		toolMenu = tk.Menu(self.menubar, tearoff=0)
		toolMenu.add_command(label="Nothing")
		toolMenu.add_command(label="Also Nothing")
		self.menubar.add_cascade(label="Tools", menu=toolMenu)

		#Create Frame for auth
		authFrame = tk.Frame(self.master, width=800, height=300)
		authFrame.pack()
		authFrame.grid_propagate(False)
		authFrame.grid_rowconfigure(0, weight=1)
		authFrame.grid_columnconfigure(0, weight=1)

		#Create Frame for world
		worldFrame = tk.Frame(self.master, width=800, height=300)
		worldFrame.pack()
		worldFrame.grid_propagate(False)
		worldFrame.grid_rowconfigure(0, weight=1)
		worldFrame.grid_columnconfigure(0, weight=1)

		# create a Text widget
		self.authPane = tk.Text(authFrame, borderwidth=3, relief="sunken")
		self.authPane.config(font=("ariel", 12), undo=True, wrap='word', state="normal")
		self.authPane.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
		self.authPane.tag_configure("role", foreground="blue", font='ariel 12 bold')

		self.worldPane = tk.Text(worldFrame, borderwidth=3, relief="sunken")
		self.worldPane.config(font=("ariel", 12), undo=True, wrap='word', state="normal")
		self.worldPane.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
		self.worldPane.tag_configure("role", foreground="green", font='ariel 12 bold')

		# create a Scrollbar and associate it with txt
		authScroll = tk.Scrollbar(authFrame, command=self.authPane.yview)
		authScroll.grid(row=0, column=1, sticky='nsew')
		self.authPane['yscrollcommand'] = authScroll.set

		worldScroll = tk.Scrollbar(worldFrame, command=self.worldPane.yview)
		worldScroll.grid(row=0, column=1, sticky='nsew')
		self.worldPane['yscrollcommand'] = worldScroll.set

	def on_closing(self):
		print("Qutting GUI")
		self.master.destroy()
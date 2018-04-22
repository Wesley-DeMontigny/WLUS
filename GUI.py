from threading import Thread, Timer
from bitstream import *
from reliability import PacketReliability
from replicamanager import *
from DBHandlers import *
from time import sleep
from GameMessage import *
from LDFReader import *
import os
from __main__ import *
import sys
from World import WorldServer
from Auth import AuthServer
import tkinter as tk
from tkinter import simpledialog


class sendToWorldDialog(simpledialog.Dialog):
	def __init__(self, parent):
		super().__init__(parent=parent)

	def body(self, master):
		self.title("Send to World")

		tk.Label(master, text="Player:").grid(row=0)
		tk.Label(master, text="World:").grid(row=1)

		self.tkvar1 = tk.StringVar(master)
		self.tkvar2 = tk.StringVar(master)
		self.players = getCharactersInGame()
		self.playerChoices = []
		self.worldChoices = []
		for i in range(self.players.__len__()):
			self.playerChoices.append(self.players[i][0])
		for i in range(Zones.zoneList.__len__()):
			self.worldChoices.append(Zones.zoneList[i][0])
		self.tkvar1.set("None")
		self.tkvar2.set("None")

		if(self.playerChoices != []):
			self.e1 = tk.OptionMenu(master, self.tkvar1, *self.playerChoices)
		else:
			self.e1 = tk.OptionMenu(master, self.tkvar1, "None")
		self.e2 = tk.OptionMenu(master, self.tkvar2, *self.worldChoices)

		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)


	def apply(self):
		player = self.tkvar1.get()
		world = self.tkvar2.get()
		if(player != "None" and world != "None"):
			worldIndex = self.worldChoices.index(world)
			self.worldID = Zones.zoneList[worldIndex][1]
			playerIndex = self.playerChoices.index(player)
			self.playerID = self.players[playerIndex][1]



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
		self.master.iconbitmap("icon.ico")
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
					self.authPane.see(tk.END)
			if(self.World != None):
				if(self.World.updateConsole == True):
					self.World.updateConsole = False
					self.worldPane.insert(tk.END, "["+self.World.role+"]", "role")
					self.worldPane.insert(tk.END, str(self.World.consoleMessage) + "\n")
					self.worldPane.see(tk.END)

	def runServer(self):
		self.World = WorldServer(("127.0.0.1", 2002), self, max_connections=10, incoming_password=b"3.25 ND1", role="WORLD")
		self.Auth = AuthServer(("127.0.0.1", 1001), self, max_connections=10, incoming_password=b"3.25 ND1", role="AUTH")

		loop = asyncio.get_event_loop()
		t = Thread(target=self.serverLoop, args=(loop,))
		t.start()

		self.menubar.entryconfig("Start Server", state="disabled")

	def logGMs(self):
		file = open(os.getcwd()+"\\Logged\\unhandledGMs.txt", "a")
		file.truncate()
		GMs = self.World.unhandledGMs
		for gm in GMs:
			file.write("Message: " + str(gm[0]) + ", Object: " + str(gm[1]) + "\n")

	def sendToWorld(self):
		win = sendToWorldDialog(parent=self.master)
		try:
			self.World.loadWorld(win.playerID, win.worldID, loadAtDefaultSpawn=True)
		except:
			print("Error while sending to world")

	def create_widgets(self):
		#Create menu items
		self.menubar.add_command(label="Start Server", command=self.runServer)

		devMenu = tk.Menu(self.menubar, tearoff=0)
		devMenu.add_command(label="Log Unhandled GMs", command=self.logGMs)
		self.menubar.add_cascade(label="Development", menu=devMenu)

		gameMenu = tk.Menu(self.menubar, tearoff=0)
		gameMenu.add_command(label="Send to World", command=self.sendToWorld)
		self.menubar.add_cascade(label="Game", menu=gameMenu)

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
		self.authPane.tag_configure("role", foreground="purple", font='ariel 12 bold')

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
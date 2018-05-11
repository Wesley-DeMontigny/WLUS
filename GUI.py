from threading import Thread, Timer
from bitstream import *
from reliability import PacketReliability
from replicamanager import *
from DBHandlers import *
from time import sleep
from GameMessage import *
from LDFReader import *
from os import listdir
from __main__ import *
import sys
import os, signal
from os.path import isfile, join
from struct import *
from World import WorldServer
from Auth import AuthServer
import tkinter as tk
from tkinter import simpledialog, filedialog


class choiceDialog(simpledialog.Dialog):
	def __init__(self, parent, label, choices):
		self.label = label
		self.choices = choices
		super().__init__(parent=parent)

	def body(self, master):
		self.title("WLUS")
		self.iconbitmap("icon.ico")
		tk.Label(master, text=self.label).grid(row=0)

		self.tkvar1 = tk.StringVar(master)
		self.tkvar1.set("None")

		self.e1 = tk.OptionMenu(master, self.tkvar1, *self.choices)

		self.e1.grid(row=0, column=1)


	def apply(self):
		self.value = self.tkvar1.get()


class sendToWorldDialog(simpledialog.Dialog):
	def __init__(self, parent, players):
		self.players = players
		super().__init__(parent=parent)

	def body(self, master):
		self.title("Send to World")
		self.iconbitmap("icon.ico")
		tk.Label(master, text="Player:").grid(row=0)
		tk.Label(master, text="World:").grid(row=1)

		self.tkvar1 = tk.StringVar(master)
		self.tkvar2 = tk.StringVar(master)
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

		self.DB_Manager = databaseManager()

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

	def onClose(self):
		print("Saving Objects to DB")
		try:
			for id in self.World.SavedObjects:
				obj = self.World.SavedObjects[id]
				components = obj.components
				# self.DB_Manager.updateWorldObject(unpack("q", components[0].objectID)[0], unpack("f", components[1].xPos)[0],
				# 								 unpack("f", components[1].yPos)[0], unpack("f", components[1].zPos)[0],
				# 								 unpack("f", components[1].xRot)[0], unpack("f", components[1].yRot)[0],
				# 								 unpack("f", components[1].zRot)[0], unpack("f", components[1].wRot)[0])
				if (unpack("l", components[0].LOT)[0] == 1):
					self.DB_Manager.setCharacterPos(unpack("q", components[0].objectID)[0], unpack("f", components[1].xPos)[0], unpack("f", components[1].yPos)[0],
												   unpack("f", components[1].zPos)[0])
		except Exception as e:
			print("Error while saving objects: ", e)

	def updateConsole(self):
		atCountWorld = 0
		atCountAuth = 0
		while True:
			if(self.Auth != None):
				try:
					message = str(self.Auth.consoleMessage[atCountAuth])
					self.authPane.insert(tk.END, "[" + self.Auth.role + "]", "role")
					self.authPane.insert(tk.END, message + "\n")
					self.authPane.see(tk.END)
					atCountAuth = atCountAuth+1
				except:
					pass
			if(self.World != None):
				try:
					message = str(self.World.consoleMessage[atCountWorld])
					self.worldPane.insert(tk.END, "["+self.World.role+"]", "role")
					self.worldPane.insert(tk.END, message + "\n")
					self.worldPane.see(tk.END)
					atCountWorld = atCountWorld+1
				except:
					pass

	def runServer(self):
		self.World = WorldServer(("127.0.0.1", 2002), self.DB_Manager, max_connections=10, incoming_password=b"3.25 ND1", role="WORLD")
		self.Auth = AuthServer(("127.0.0.1", 1001), self.DB_Manager, max_connections=10, incoming_password=b"3.25 ND1", role="AUTH")

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

	def testWorldFunction(self):
		t = Thread(target=self.World.test)
		t.start()

	def sendToWorld(self):
		win = sendToWorldDialog(parent=self.master, players=self.DB_Manager.getCharactersInGame())
		session = self.DB_Manager.getSessionByCharacter(win.playerID)
		try:
			self.World.loadWorld(win.playerID, win.worldID, (str(session[2]), int(session[7])), loadAtDefaultSpawn=True)
		except Exception as e:
			print("Error While Sending to World: " + str(e))

	def spawnObjectAtPlayer(self):
		connections = self.World._connected
		names = []
		for key, value in connections.items():
			names.append(str(self.DB_Manager.getPlayerNameFromConnection(key[0], key[1])[0]))
		nameChoice = choiceDialog(self.master, "Player", names)
		playerName = nameChoice.value
		playerID = int(self.DB_Manager.getObjectIDFromName(playerName)[0])
		lot = int(simpledialog.askfloat("Input", "What is the Object LOT?", parent=self.master))
		zone = int(self.DB_Manager.getZoneOfObject(playerID)[0])
		objID = randint(100000000000000000, 999999999999999999)
		self.World.createObject("", lot, objID, zone, unpack("f", self.World.SavedObjects[playerID].components[1].xPos)[0],
								unpack("f", self.World.SavedObjects[playerID].components[1].yPos)[0],
								unpack("f", self.World.SavedObjects[playerID].components[1].zPos)[0], 0, 0, 0, 0, Register=False)


	def sendPacketFromFile(self):
		packet = BitStream()
		connections = self.World._connected
		names = []
		for key, value in connections.items():
			names.append(str(self.DB_Manager.getPlayerNameFromConnection(key[0], key[1])[0]))
		nameChoice = choiceDialog(self.master, "Player", names)
		playerName = nameChoice.value
		session = self.DB_Manager.getSessionByPlayerName(playerName)
		f = filedialog.askopenfile("rb", filetypes=(("Binary Files", "*.bin"), ("All files", "*.*") ))
		packet.write(f.read())
		self.World.send(packet, (str(session[2]), int(session[7])))

	def giveFlight(self):
		connections = self.World._connected
		names = []
		for key, value in connections.items():
			names.append(str(self.DB_Manager.getPlayerNameFromConnection(key[0], key[1])[0]))
		nameChoice = choiceDialog(self.master, "Player", names)
		playerName = nameChoice.value
		objectID = int(self.DB_Manager.getObjectIDFromName(playerName)[0])
		self.World.SetJetPackMode(objectID, bypassChecks=True)

	def registerAccount(self):
		username = simpledialog.askstring("Input", "Username: ", parent=self.master)
		password = simpledialog.askstring("Input", "Password: ", parent=self.master)
		if(password != None and username != None):
			try:
				self.DB_Manager.registerAccount(username, password)
			except:
				pass

	def create_widgets(self):
		#Create menu items
		self.menubar.add_command(label="Start Server", command=self.runServer)

		devMenu = tk.Menu(self.menubar, tearoff=0)
		devMenu.add_command(label="Log Unhandled GMs", command=self.logGMs)
		devMenu.add_command(label="Send Packet From File", command=self.sendPacketFromFile)
		devMenu.add_command(label="Test Function", command=self.testWorldFunction)
		self.menubar.add_cascade(label="Development", menu=devMenu)

		gameMenu = tk.Menu(self.menubar, tearoff=0)
		gameMenu.add_command(label="Register Account", command=self.registerAccount)
		gameMenu.add_command(label="Send to World", command=self.sendToWorld)
		gameMenu.add_command(label="Fly", command=self.giveFlight)
		gameMenu.add_command(label="Spawn Object At Player", command=self.spawnObjectAtPlayer)
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
		print("Qutting")
		self.onClose()
		os.kill(os.getpid(), signal.SIGTERM)
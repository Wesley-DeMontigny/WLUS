from pyraknet.messages import Address
from pyraknet.bitstream import *
import random
from Enum import SessionState, ZoneID

class GameObject():
	def __init__(self, Parent):
		self.Parent = Parent
		self.ObjectConfig : dict = {"LOT":0,"ObjectID":None,"Name":None}
		self.Tag : str = None

class Zone():
	def __init__(self, Parent):
		self.ZoneID : ZoneID = None
		self.Parent = Parent
		self.Objects : list = []
		self.SpawnLocation : Vector3 = Vector3(0,0,0)
		self.ActivityWorld : bool = False
	def createObject(self, Object : GameObject):
		if(Object.ObjectConfig["ObjectID"] == None):
			Object.ObjectConfig["ObjectID"] = random.randint(100000000000000000, 999999999999999999)
		self.Objects.append(Object)
	def getObjectByName(self, Name : str):
		for Object in self.Objects:
			if(Object.ObjectConfig["Name"] == Name):
				return Object
		return None
	def getObjectByID(self, ID : int):
		for Object in self.Objects:
			if(Object.ObjectConfig["ObjectID"] == ID):
				return Object
		return None
	def deleteObject(self, Object : GameObject):
		for GameObject in self.Objects:
			if(Object == GameObject):
				del GameObject


class Vector3():
	def __init__(self, X : float, Y : float, Z : float):
		self.X : float = X
		self.Y : float = Y
		self.Z : float = Z
	def translate(self, X : float, Y : float, Z : float):
		self.X += X
		self.Y += Y
		self.Z += Z
	def set(self, X : float, Y : float, Z : float):
		self.X = X
		self.Y = Y
		self.Z = Z

class Vector4():
	def __init__(self, X : float, Y : float, Z : float, W : float):
		self.X : float = X
		self.Y : float = Y
		self.Z : float = Z
		self.W : float = W
	def translate(self, X : float, Y : float, Z : float, W : float):
		self.X += X
		self.Y += Y
		self.Z += Z
		self.W += W
	def set(self, X : float, Y : float, Z : float, W : float):
		self.X = X
		self.Y = Y
		self.Z = Z
		self.W = W

class ReplicaObject(GameObject):
	def __init__(self, Parent):
		super().__init__(Parent)
		self.Components = []
		self.ObjectConfig["Position"] = Vector3(0,0,0)
		self.ObjectConfig["Rotation"] = Vector4(0,0,0,0)

	def write_construction(self, stream: WriteStream):
		for Component in self.Components:
			stream.write(Component.construct(self.ObjectConfig))

	def serialize(self, stream: WriteStream):
		for Component in self.Components:
			stream.write(Component.serialize(self.ObjectConfig))

	def on_destruction(self):
		print("Destroying Object {}".format(self.ObjectConfig["ObjectID"]))

class Session():
	def __init__(self, Parent):
		self.Parent = Parent
		self.ZoneID : int = None
		self.ObjectID : int = None
		self.userKey : str = None
		self.accountUsername : str = None
		self.address : Address = None
		self.isAdmin : bool = False
		self.State : SessionState = None

class Mission():
	def __init__(self, Parent):
		self.Parent : Character = Parent
		self.MissionType : str = None
		self.MissionID : int = 0
		self.RewardCurrency : int = 0
		self.RewardItems : list = []
		self.RewardUniverseScore : int = 0
		self.Offerer : int = 0
		self.Target : int = 0
		self.Progress : int = 0
	def Complete(self):
		self.Parent.UniverseScore += self.RewardUniverseScore
		self.Parent.Currency += self.RewardCurrency
		for item in self.RewardItems:
			self.Parent.Inventory.addItem(item)
		self.Parent.CompletedMissionIDs.append(self.MissionID)
		try:
			for i in range(len(self.Parent.CurrentMissions)):
				if(self.Parent.CurrentMissions[i] == self):
					del self.Parent.CurrentMissions[i]
		except:
			pass


class Character(ReplicaObject):
	def __init__(self, Parent):
		super().__init__(Parent)
		self.Zone : int = 0
		self.CurrentMissions : list = []
		self.CompletedMissionIDs : list = []
		self.Level : int = 0
		self.UniverseScore : int = 0
		self.Currency : int = 0
		self.ObjectConfig["LOT"] = 1
		self.ObjectConfig["ShirtColor"] = 0
		self.ObjectConfig["ShirtStyle"] = 0
		self.ObjectConfig["PantsColor"] = 0
		self.ObjectConfig["HairColor"] = 0
		self.ObjectConfig["HairStyle"] = 0
		self.ObjectConfig["lh"] = 0
		self.ObjectConfig["rh"] = 0
		self.ObjectConfig["Eyebrows"] = 0
		self.ObjectConfig["Eyes"] = 0
		self.ObjectConfig["Mouth"] = 0
		self.Inventory : Inventory = Inventory(self)

class Inventory():
	def __init__(self, Parent):
		self.Parent = Parent
		self.InventoryList = []
		self.Space = 24
	def addItem(self, LOT : int, Slot : int = None, Equipped : bool = False, Linked : bool = False, Quantity : int = 1, ObjectID : int = random.randint(100000000000000000, 999999999999999999)):
		if(Slot != None):
			self.InventoryList.append({"LOT":LOT, "Slot":Slot, "Equipped":Equipped, "Linked":Linked, "Quantity":Quantity, "ObjectID":ObjectID})
		else:
			takenSlots = []
			for item in self.InventoryList:
				takenSlots.append(item["Slot"])
			for i in range(self.Space):
				if(i not in takenSlots):
					self.InventoryList.append({"LOT": LOT, "Slot": i, "Equipped": Equipped, "Linked":Linked, "Quantity":Quantity, "ObjectID":ObjectID})
					return
			print("No Space Left In Inventory!")
	def getEquippedItems(self):
		equippedItems = []
		for item in self.InventoryList:
			if(item["Equipped"] == True):
				equippedItems.append(item)
		return equippedItems


class GameManager():
	def __init__(self):
		self.Sessions : list = []
		self.AccountManager = None
		self.Zones : list = []

	def purgePlayers(self):
		for Zone in self.Zones:
			for Object in Zone.Objects:
				if(Object.ObjectConfig["ObjectID"] == 1):
					del Object

	def registerSession(self, Session : Session):
		self.Sessions.append(Session)

	def getSessionByAddress(self, address):
		for session in self.Sessions:
			if(session.address == address):
				return session
		return None

	def clearSessions(self):
		self.Sessions = []

	def getAccountByUsername(self, Username : str):
		return self.AccountManager.getAccountByUsername(Username)

	def getCharacterByObjectID(self, ObjectID : int):
		return self.AccountManager.getCharacterByObjectID(ObjectID)

	def getSessionByCharacterID(self, characterID):
		for session in self.Sessions:
			if(session.character.objectID == characterID):
				return session
		return None

	def clearZones(self):
		self.Zones = []

	def getZoneByID(self, ZoneID : ZoneID):
		for Zone in self.Zones:
			if(Zone.ZoneID == ZoneID):
				return Zone
		return None

	def registerZone(self, ZoneObject : Zone):
		for Zone in self.Zones:
			if(Zone.ZoneID == ZoneObject.ZoneID):
				print("Canceled New Zone Registration of Zone {} Because it Already Existed!".format(ZoneObject.ZoneID))
				return Exception
		self.Zones.append(ZoneObject)

	def getSessionByUsername(self, username):
		for session in self.Sessions:
			if(session.accountUsername == username):
				return session
		return None
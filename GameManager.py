from passlib.hash import sha256_crypt
from pyraknet.replicamanager import Replica
from pyraknet.messages import Address
from pyraknet.bitstream import *
import random
from Enum import SessionState, ZoneID
from ServerUtilities import getPantsID, getShirtID


class GameObject():
	def __init__(self, Parent):
		self.Parent = Parent
		self.ObjectID : int = 0
		self.LOT : int = 0
		self.Name : str = None
		self.Tag : str = None

class Spawner(GameObject):
	def __init__(self, Parent):
		super().__init__(Parent)
		self.Tag = "Spawner"
		self.SpawnedObject : GameObject = None

class Zone():
	def __init__(self, Parent):
		self.ZoneID : ZoneID = None
		self.Parent = Parent
		self.Objects : list = []
	def createObject(self, Object : GameObject):
		if(Object.ObjectID == None):
			Object.ObjectID = random.randint(100000000000000000, 999999999999999999)
		self.Objects.append(Object)
	def getObjectByName(self, Name : str):
		for Object in self.Objects:
			if(Object.Name == Name):
				return Object
		return None
	def getObjectByID(self, ID : int):
		for Object in self.Objects:
			if(Object.ObjectID == ID):
				return Object
		return None
	def deleteObject(self, Object : GameObject):
		for GameObject in self.Objects:
			if(Object == GameObject):
				del GameObject


class Vector3():
	def __init__(self, X : int, Y : int, Z : int):
		self.X : int = X
		self.Y : int = Y
		self.Z : int = Z
	def translate(self, X : int, Y : int, Z : int):
		self.X += X
		self.Y += Y
		self.Z += Z
	def set(self, X : int, Y : int, Z : int):
		self.X = X
		self.Y = Y
		self.Z = Z

class Vector4():
	def __init__(self, X : int, Y : int, Z : int, W : int):
		self.X : int = X
		self.Y : int = Y
		self.Z : int = Z
		self.W : int = W
	def translate(self, X : int, Y : int, Z : int, W : int):
		self.X += X
		self.Y += Y
		self.Z += Z
		self.W += W
	def set(self, X : int, Y : int, Z : int, W : int):
		self.X = X
		self.Y = Y
		self.Z = Z
		self.W = W

class ReplicaObject(GameObject):
	def __init__(self, Parent):
		super().__init__(Parent)
		self.ReplicaComponents : list = []
		self.ObjectConfig : dict = {"Position": Vector3(0,0,0), "Rotation": Vector4(0,0,0,0)}
		self.Replica : GameReplica = GameReplica()
	def initializeReplica(self):
		self.Replica.setComponents(self.ReplicaComponents)

class GameReplica(Replica):
	def __init__(self):
		self.Components = None
	def setComponents(self, Components):
		self.Components = Components
	def write_construction(self, stream: WriteStream):
		for Component in self.Components:
			stream.write(Component.construct())
	def serialize(self, stream: WriteStream):
		for Component in self.Components:
			stream.write(Component.serialize())
	def on_destruction(self):
		"""Not sure what to put here yet"""

class ReplicaComponent():
	def __init__(self, Parent):
		self.Parent = Parent
		self.Name = None
	def construct(self) -> None:
		raise NotImplementedError
	def serialize(self) -> None:
		raise NotImplementedError

class Session():
	def __init__(self, Parent):
		self.Parent = Parent
		self.ZoneID : int = None
		self.character : Character = None
		self.userKey : str = None
		self.accountUsername : str = None
		self.address : Address = None
		self.isAdmin : bool = False
		self.State : SessionState = None

class Account():
	def __init__(self, Parent):
		self.Parent = Parent
		self.Username : str = None
		self.Password : str = None
		self.Banned : bool = False
		self.Characters : list = []
	def CreateMinifigure(self, Name : str, ShirtColor : int, ShirtStyle : int, PantsColor : int, HairColor : int, HairStyle : int, lh : int, rh : int, Eyebrows : int, Eyes : int, Mouth : int):
		Minifigure = Character(self)
		Minifigure.Name = Name
		Minifigure.ShirtColor = ShirtColor
		Minifigure.ShirtStyle = ShirtStyle
		Minifigure.PantsColor = PantsColor
		Minifigure.HairColor = HairColor
		Minifigure.HairStyle = HairStyle
		Minifigure.lh = lh
		Minifigure.rh = rh
		Minifigure.ObjectID = random.randint(100000000000000000, 999999999999999999)
		Minifigure.Eyebrows = Eyebrows
		Minifigure.Eyes = Eyes
		Minifigure.Mouth = Mouth
		shirtLOT = getShirtID(ShirtColor, ShirtStyle)
		pantsLOT = getPantsID(PantsColor)
		Minifigure.Inventory.addItem(shirtLOT, Equipped=True)
		Minifigure.Inventory.addItem(pantsLOT, Equipped=True)
		self.Characters.append(Minifigure)

class Character(ReplicaObject):
	def __init__(self, Parent):
		super().__init__(Parent)
		self.Zone : int = 0
		self.LOT = 1
		self.ShirtColor : int = 0
		self.ShirtStyle : int = 0
		self.PantsColor : int = 0
		self.HairColor : int = 0
		self.HairStyle : int = 0
		self. lh : int = 0
		self.rh : int = 0
		self.Eyebrows : int = 0
		self.Eyes : int = 0
		self.Mouth : int = 0
		self.Inventory : Inventory = Inventory(self)

class Inventory():
	def __init__(self, Parent):
		self.Parent = Parent
		self.InventoryList = []
		self.Space = 24
	def addItem(self, LOT : int, Slot : int = None, Equipped : bool = False, Linked : bool = False):
		if(Slot != None):
			self.InventoryList.append({"LOT":LOT, "Slot":Slot, "Equipped":Equipped, "Linked":Linked})
		else:
			takenSlots = []
			for item in self.InventoryList:
				takenSlots.append(item["Slot"])
			for i in range(self.Space):
				if(i not in takenSlots):
					self.InventoryList.append({"LOT": LOT, "Slot": i, "Equipped": Equipped, "Linked":Linked})
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
		self.Accounts : list = []
		self.Zones : list = []

	def getAccountByUsername(self, Username : str):
		for Account in self.Accounts:
			if(Account.Username == Username):
				return Account
		return None

	def purgePlayers(self):
		for Zone in self.Zones:
			for Object in Zone.Objects:
				if(Object.LOT == 1):
					del Object

	def registerAccount(self, Username : str, Password : str):
		account = Account(self)
		account.Username = Username
		account.Password = sha256_crypt.encrypt(Password)
		account.Banned = False
		self.Accounts.append(account)

	def registerSession(self, Session : Session):
		self.Sessions.append(Session)

	def getSessionByAddress(self, address):
		for session in self.Sessions:
			if(session.address == address):
				return session
		return None

	def clearSessions(self):
		self.Sessions = []

	def getSessionByCharacterID(self, characterID):
		for session in self.Sessions:
			if(session.character.objectID == characterID):
				return session
		return None

	def clearZones(self):
		self.Zones = []

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
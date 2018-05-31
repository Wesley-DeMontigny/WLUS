from pyraknet.messages import Address
from pyraknet.bitstream import *
import random
from typing import Callable
from Enum import SessionState, ZoneID, ReplicaTypes
from GameDB import *
from ObjectConstructor import WriteReplica
from structures import Vector3, Vector4
from PlayerEventHandlers import *
import threading

def Nothing(*args):
	pass

class GameObject():
	def __init__(self, Parent):
		self.Parent = Parent
		self.ObjectConfig : dict = {"LOT":0,"ObjectID":None,"Name":None}
		self.EventHandlers : dict = {}
		self.Tag : str = None
	def HandleEvent(self, EventID : str, Stream : ReadStream, address : Address, Server : GameServer):
		if(EventID in self.EventHandlers):
			eventThread = threading.Thread(target=self.EventHandlers[EventID], args=[self, Stream, address, Server])
			eventThread.start()
		else:
			print("Object {} Has No Handler For Event {}".format(self.ObjectConfig["ObjectID"], EventID))
	def RegisterEvent(self, EventID : str, Handler : Callable):
		self.EventHandlers[EventID] = Handler

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


class ReplicaObject(GameObject):
	def __init__(self, Parent):
		super().__init__(Parent)
		self.Components = []
		self.ObjectConfig["Position"] = None
		self.ObjectConfig["Rotation"] = Vector4(0,0,0,0)
		self.ObjectConfig["Scale"] = 1
		self.ObjectConfig["SpawnerID"] = None

	def write_construction(self, stream: WriteStream):
		WriteReplica(stream, self.Components, self.ObjectConfig, ReplicaTypes.Construction)

	def serialize(self, stream: WriteStream):
		WriteReplica(stream, self.Components, self.ObjectConfig, ReplicaTypes.Serialization)

	def on_destruction(self):
		print("Destroying Object {}".format(self.ObjectConfig["ObjectID"]))

	def findComponentsFromCDClient(self, CDClient : GameDB):
		componentsRegistry : DBTable = CDClient.Tables["ComponentsRegistry"]
		components = componentsRegistry.select(["component_type"], "id = {}".format(self.ObjectConfig["LOT"]))
		compList = []
		for row in components:
			compList.append(row["component_type"])
		return compList

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

class CharacterStatistics():
	def __init__(self):
		self.CurrencyCollected : int = 0
		self.BricksCollected : int = 0
		self.SmashablesSmashed: int = 0
		self.QuickBuildsDone: int = 0
		self.EnemiesSmashed: int = 0
		self.RocketsUsed : int = 0
		self.PetsTamed : int = 0
		self.ImaginationCollected : int = 0
		self.HealthCollected : int = 0
		self.ArmorCollected : int = 0
		self.DistanceTraveled : int = 0
		self.TimesDied : int = 0
		self.DamageTaken : int = 0
		self.DamageHealed : int = 0
		self.ArmorRepaired : int = 0
		self.ImaginationRestored : int = 0
		self.ImaginationUsed : int = 0
		self.DistanceDriven : int = 0
		self.TimeAirborneInCar : int = 0
		self.RacingImaginationCollected : int = 0
		self.RacingImaginationCratesSmashed : int = 0
		self.RaceCarBoosts : int = 0
		self.RacingSmashablesSmashed : int = 0
		self.RacesFinished : int = 0
		self.RacesWon : int = 0
		self.CarWrecks : int = 0

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
		self.Parent.ObjectConfig["UniverseScore"] += self.RewardUniverseScore
		self.Parent.ObjectConfig["Currency"] += self.RewardCurrency
		for item in self.RewardItems:
			self.Parent.ObjectConfig["Inventory"].addItem(item)
		self.Parent.ObjectConfig["CompletedMissions"].append(self.MissionID)
		try:
			for i in range(len(self.Parent.ObjectConfig["CurrentMissions"])):
				if(self.Parent.ObjectConfig["CurrentMissions"][i] == self):
					del self.Parent.ObjectConfig["CurrentMissions"][i]
		except:
			pass

class Humanoid(ReplicaObject):
	def __init__(self, Parent):
		super().__init__(Parent)
		self.ObjectConfig["Health"] = 1
		self.ObjectConfig["MaxHealth"] = 1
		self.ObjectConfig["Armor"] = 0
		self.ObjectConfig["MaxArmor"] = 0
		self.ObjectConfig["Imagination"] = 0
		self.ObjectConfig["MaxImagination"] = 0
		self.ObjectConfig["Faction"] = 0
		self.ObjectConfig["isSmashable"] = True

	def Damage(self, amount):
		self.ObjectConfig["Health"] -= amount

class Character(Humanoid):
	def __init__(self, Parent):
		super().__init__(Parent)
		self.Zone : int = 0
		self.ObjectConfig["CurrentMissions"] = []
		self.ObjectConfig["CompletedMissions"] = []
		self.ObjectConfig["Level"] = 0
		self.ObjectConfig["AccountID"] = Parent.AccountID
		self.ObjectConfig["UniverseScore"] = 0
		self.ObjectConfig["Currency"] = 0
		self.ObjectConfig["CharacterStatistics"] = CharacterStatistics()
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
		self.ObjectConfig["Velocity"] = Vector3(0,0,0)
		self.ObjectConfig["AngularVelocity"] = Vector3(0,0,0)
		self.ObjectConfig["OnGround"] = False
		self.ObjectConfig["MaxHealth"] = 4
		self.ObjectConfig["Health"] = 4
		self.ObjectConfig["Faction"] = 1
		self.ObjectConfig["isSmashable"] = False
		self.ObjectConfig["Alive"] = True
		self.ObjectConfig["Inventory"] = Inventory(self)

		self.RegisterEvent("GM_04b2", RemoveHealth)#Request Death
		self.RegisterEvent("GM_05cd", Nothing)#Modified Ghosting
		self.RegisterEvent("GM_0378", Nothing)#Ready For Updates
		self.RegisterEvent("GM_01f9", PlayerLoaded)#Player Loaded
		self.RegisterEvent("GM_09f", Ressurect)#Ressurect Request
		self.RegisterEvent("GM_0300", Nothing)#Set Ghosting Distance


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
		purgeCount = 0
		for Zone in self.Zones:
			for i in range(len(Zone.Objects)):
				Object = Zone.Objects[i]
				if(Object.ObjectConfig["LOT"] == 1):
					del Zone.Objects[i]
					purgeCount += 1
		print("Purged {} Players From Game".format(purgeCount))


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

	def getObjectByID(self, ObjectID : int):
		for Zone in self.Zones:
			for GameObject in Zone.Objects:
				if(GameObject.ObjectConfig["ObjectID"] == ObjectID):
					return GameObject
		return None

	def deleteObjectByID(self, ObjectID : int):
		for Zone in self.Zones:
			for i in range(len(Zone.Objects)):
				if(Zone.Objects[i].ObjectConfig["ObjectID"] == ObjectID):
					if(Zone.Objects[i] is ReplicaObject):
						Zone.Objects[i].on_destruction()
					del Zone.Objects[i]
		return None

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

	def getConnectionsInZone(self, ZoneID : ZoneID):
		connectionList = []
		for session in self.Sessions:
			if(session.ZoneID == ZoneID):
				connectionList.append(session.address)
		return connectionList

	def getPlayers(self):
		playerList = []
		for Zone in self.Zones:
			for Object in Zone.Objects:
				if(Object.ObjectConfig["LOT"] == 1):
					playerList.append(Object)
		return playerList


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
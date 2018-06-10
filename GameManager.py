from pyraknet.messages import Address
from pyraknet.bitstream import *
import random
import time
from typing import Callable
from Enum import *
from GameDB import *
from ObjectConstructor import WriteReplica
from structures import Vector3, Vector4
from ObjectEventHandlers import *
from PlayerEventHandlers import *
import threading
import LVLFiles

def Nothing(*args):
	pass

class GameObject():
	def __init__(self, Parent):
		self.Parent = Parent
		self.ObjectConfig : dict = {"LOT":0,"ObjectID":None,"Name":""}
		self.EventHandlers : dict = {}
		self.Tag : str = ""
	def HandleEvent(self, EventID : str, Stream : ReadStream, address : Address, Server : GameServer):
		if(EventID in self.EventHandlers):
			eventThread = threading.Thread(target=self.EventHandlers[EventID], args=[self, Stream, address, Server])
			eventThread.start()
		else:
			#print("Object {} Has No Handler For Event {}".format(self.ObjectConfig["ObjectID"], EventID))
			pass
	def RegisterEvent(self, EventID : str, Handler : Callable):
		self.EventHandlers[EventID] = Handler

class Zone():
	def __init__(self, Parent):
		self.ZoneID : ZoneID = None
		self.Parent = Parent
		self.Objects : list = []
		self.SpawnLocation : Vector3 = Vector3(0,0,0)
		self.ActivityWorld : bool = False
		self.ZoneName : str = ""
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
		self.ObjectConfig["ObjectType"] = ""
		self.ObjectConfig["Position"] = Vector3(0,0,0)
		self.ObjectConfig["Rotation"] = Vector4(0,0,0,0)
		self.ObjectConfig["Scale"] = 1
		self.ObjectConfig["SpawnerID"] = None

		self.ObjectConfig["NeedsUpdate"] = False

	def write_construction(self, stream: WriteStream):
		WriteReplica(stream, self.Components, self.ObjectConfig, ReplicaTypes.Construction)

	def serialize(self, stream: WriteStream):
		WriteReplica(stream, self.Components, self.ObjectConfig, ReplicaTypes.Serialization)

	def on_destruction(self):
		pass

	def getObjectType(self, CDClient : GameDB):
		return CDClient.Tables["Objects"].select(["type"], "id = {}".format(self.ObjectConfig["LOT"]))[0]["type"]

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
		self.TaskType : int = 0
		self.RewardCurrency : int = 0
		self.RewardItems : list = []
		self.RewardUniverseScore : int = 0
		self.Offerer : int = 0
		self.Target : int = 0
		self.Progress : int = 0
		self.Prereq = []
	def Complete(self):
		self.Parent.ObjectConfig["UniverseScore"] += self.RewardUniverseScore
		self.Parent.ObjectConfig["Currency"] += self.RewardCurrency
		for item in self.RewardItems:
			itemId = random.randint(100000000000000000, 999999999999999999)
			self.Parent.ObjectConfig["Inventory"].addItem(item, itemId)

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
		self.ObjectConfig["LootIndex"] = None
		self.ObjectConfig["CurrencyIndex"] = None
		self.ObjectConfig["HumanoidLevel"] = None

	def Damage(self, amount):
		self.ObjectConfig["Health"] -= amount
		self.ObjectConfig["NeedsUpdate"] = True

	def Kill(self, **args):
		print("Killed Object {}".format(self.ObjectConfig["ObjectID"]))

	def setDestructible(self, CDClient : GameDB):
		try:
			ComponentID = CDClient.Tables["ComponentsRegistry"].select(["component_id"], "id = {} AND component_type = 7".format(self.ObjectConfig["LOT"]))
			DestructibleComp = CDClient.Tables["DestructibleComponent"].select(["faction", "level", "LootMatrixIndex",
																				"CurrencyIndex", "life", "armor", "imagination", "isSmashable"], "id = {}".format(ComponentID[0]["component_id"]))[0]
		except:
			return
		if(DestructibleComp["faction"] is not None):
			self.ObjectConfig["Faction"] = int(DestructibleComp["faction"])

		if (DestructibleComp["level"] is not None and int(DestructibleComp["level"]) != -1):
			self.ObjectConfig["HumanoidLevel"] = int(DestructibleComp["level"])

		if(DestructibleComp["LootMatrixIndex"] is not None):
			self.ObjectConfig["LootIndex"] = int(DestructibleComp["LootMatrixIndex"])

		if(DestructibleComp["CurrencyIndex"] is not None):
			self.ObjectConfig["CurrencyIndex"] = int(DestructibleComp["CurrencyIndex"])

		if (DestructibleComp["life"] is not None and int(DestructibleComp["life"]) != -1):
			self.ObjectConfig["Health"] = int(DestructibleComp["life"])
			self.ObjectConfig["MaxHealth"] = int(DestructibleComp["life"])

		if (DestructibleComp["armor"] is not None and int(DestructibleComp["armor"]) != -1):
			self.ObjectConfig["Armor"] = int(DestructibleComp["armor"])
			self.ObjectConfig["MaxArmor"] = int(DestructibleComp["armor"])

		if (DestructibleComp["imagination"] is not None and int(DestructibleComp["imagination"]) != -1):
			self.ObjectConfig["Imagination"] = int(DestructibleComp["imagination"])
			self.ObjectConfig["MaxImagination"] = int(DestructibleComp["imagination"])

		if (DestructibleComp["isSmashable"] is not None):
			self.ObjectConfig["isSmashable"] = bool(DestructibleComp["isSmashable"])

class Smashable(Humanoid):
	def __init__(self, Parent):
		super().__init__(Parent)
		self.ObjectConfig["isSmashable"] = True
		self.ObjectConfig["Faction"] = 6

class Enemy(Humanoid):
	def __init__(self, Parent):
		super().__init__(Parent)
		self.ObjectConfig["OnGround"] = True
		self.ObjectConfig["Velocity"] = Vector3(0,0,0)
		self.ObjectConfig["AngularVelocity"] = Vector4(0,0,0,0)
		self.ObjectConfig["isSmashable"] = True
		self.ObjectConfig["Faction"] = 4

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
		self.ObjectConfig["LoadingIn"] = True
		self.ObjectConfig["PVPEnabled"] = False

		self.ObjectConfig["GhostingDistance"] = 250
		self.ClientObjects : list = []

		self.RegisterEvent("GM_04b2", SmashPlayer)#Request Death
		self.RegisterEvent("GM_05cd", Nothing)#Modify Ghosting Distance
		self.RegisterEvent("GM_0378", Nothing)#Ready For Updates
		self.RegisterEvent("GM_01f9", PlayerLoaded)#Player Loaded
		self.RegisterEvent("GM_09f", Ressurect)#Ressurect Request
		self.RegisterEvent("GM_0300", Nothing)#Set Ghosting Distance
		self.RegisterEvent("GM_0352", RunCommand)#Run chat command
		self.RegisterEvent("GM_016c", HandleInteraction)#Handles Interaction Request

	def Kill(self, Server : GameServer):
		super().Kill()
		killPacket = WriteStream()
		Server.InitializeGameMessage(killPacket, self.ObjectConfig["ObjectID"], 0x0025)
		Server.brodcastPacket(killPacket, Server.Game.getObjectByID(self.ObjectConfig["ObjectID"]).Zone)

	def getMissionByID(self, MissionID):
		for mission in self.ObjectConfig["CurrentMissions"]:
			if(mission.MissionID == MissionID):
				return mission
		return None

	def giveMission(self,  missionRow : dict, taskType : int):
		missionObj = Mission(self)
		missionObj.Offerer = int(missionRow["offer_objectID"])
		missionObj.TaskType = taskType
		missionObj.Target = int(missionRow["target_objectID"])
		missionObj.MissionID = int(missionRow["id"])
		missionObj.MissionType = str(missionRow["defined_type"])
		missionObj.RewardUniverseScore = int(missionRow["LegoScore"])
		missionObj.RewardCurrency = int(missionRow["reward_currency"])
		missionObj.Prereq = str(missionRow["prereqMissionID"]).split("|")
		if (int(missionRow["reward_item1"]) != -1):
			for _ in range(int(missionRow["reward_item1_count"])):
				missionObj.RewardItems.append(int(missionRow["reward_item1"]))
		if (int(missionRow["reward_item2"]) != -1):
			for _ in range(int(missionRow["reward_item2_count"])):
				missionObj.RewardItems.append(int(missionRow["reward_item2"]))
		if (int(missionRow["reward_item3"]) != -1):
			for _ in range(int(missionRow["reward_item3_count"])):
				missionObj.RewardItems.append(int(missionRow["reward_item3"]))
		if (int(missionRow["reward_item4"]) != -1):
			for _ in range(int(missionRow["reward_item4_count"])):
				missionObj.RewardItems.append(int(missionRow["reward_item4"]))
		self.ObjectConfig["CurrentMissions"].append(missionObj)

class Inventory():
	def __init__(self, Parent):
		self.Parent = Parent
		self.InventoryList = []
		self.Space = 20
	def addItem(self, LOT : int,  ObjectID : int, Slot : int = None, Equipped : bool = False, Linked : bool = False, Quantity : int = 1):
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
	def getItemByID(self, ObjectID : int):
		for item in self.InventoryList:
			if(item["ObjectID"] == ObjectID):
				return item
		return None

class GameManager():
	def __init__(self):
		self.Sessions : list = []
		self.AccountManager = None
		self.Zones : list = []

	def purgePlayers(self):
		purgeCount = 0
		for Zone in self.Zones:
			for object in Zone.Objects:
				if(object.ObjectConfig["LOT"] == 1):
					del Zone.Objects[Zone.Objects.index(object)]
					purgeCount += 1
		#print("Purged {} Players From Game".format(purgeCount))


	def registerSession(self, Session : Session):
		self.Sessions.append(Session)

	def getSessionByAddress(self, address):
		for session in self.Sessions:
			if(session.address == address):
				return session
		return None

	def clearSessions(self):
		self.Sessions = []

	def getObjectZone(self, Object : GameObject):
		for zone in self.Zones:
			if(Object in zone.Objects):
				return zone.ZoneID
		return None

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
			if(session.ObjectID == characterID):
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


	def registerZone(self, ZoneObject : Zone, lvlFiles : list, Server : GameServer):
		for Zone in self.Zones:
			if(Zone.ZoneID == ZoneObject.ZoneID):
				print("Canceled New Zone Registration of '{}' Because it Already Existed!".format(ZoneNames[ZoneObject.ZoneID]))
				return Exception
		self.Zones.append(ZoneObject)
		for file in lvlFiles:
			lvl = LVLFiles.lvlFile(file)
			for object in lvl.Objects:
				if("spawntemplate" in object["LDF"]):
					respawn = None
					renderDisabled = False
					if("renderDisabled" in object["LDF"] and object["LDF"]["renderDisabled"] == '1'):
						renderDisabled = True
					if("respawn" in object["LDF"]):
						respawn = float(object["LDF"]["respawn"])
					Server.spawnObject(int(object["LDF"]["spawntemplate"]), ZoneObject.ZoneID, {"Scale":int(object["Scale"]),
																								"SpawnerID":int(object["ObjectID"]),
																								"Respawn":respawn, "Render":not renderDisabled}, object["Position"], object["Rotation"], debug=False, initialize=True)
					time.sleep(.05)
	def killPlayer(self, Server: GameServer, PlayerID: int):
		killPacket = WriteStream()
		Server.InitializeGameMessage(killPacket, PlayerID, 0x0025)
		Server.brodcastPacket(killPacket, self.getObjectByID(PlayerID).Zone)

	def getSessionByUsername(self, username):
		for session in self.Sessions:
			if(session.accountUsername == username):
				return session
		return None
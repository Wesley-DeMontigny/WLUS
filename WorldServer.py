from typing import Callable
import WorldPackets
from PacketHeaders import PacketHeader
from Enum import *
from GameManager import *
from GameDB import GameDB
import threading
from ServerUtilities import *
import pyraknet
from structures import Vector3, Vector4
from pyraknet.replicamanager import *
from core import GameServer, GameReplicaManager
from time import sleep
import threading
import LVLFiles

class WorldServer(GameServer):
	def __init__(self, address: Address, max_connections: int, incoming_password: bytes, GameManager : GameManager, CDClient : GameDB, ServerDB : GameDB):
		super().__init__(address, max_connections, incoming_password, GameManager, CDClient, ServerDB)
		self.add_handler(pyraknet.server.Event.UserPacket, self.handlePacket)
		self.add_handler(pyraknet.server.Event.Disconnect, self.handleWorldDisconnect)
		self.WorldHandlers = {}
		self.ReplicaManagers = {}

		self.registerWorldHandler(PacketHeader.ClientUserSessionInfo.value, WorldPackets.HandleSessionKey)
		self.registerWorldHandler(PacketHeader.ClientMinifigureListRequest.value, WorldPackets.HandleMinifigListRequest)
		self.registerWorldHandler(PacketHeader.ClientMinifigureCreateRequest.value, WorldPackets.HandleMinifigureCreation)
		self.registerWorldHandler(PacketHeader.ClientDeleteMinifigureRequest.value, WorldPackets.HandleMinifigureDeletion)
		self.registerWorldHandler(PacketHeader.ClientEnterWorld.value, WorldPackets.HandleJoinWorld)
		self.registerWorldHandler(PacketHeader.RoutedPacket.value, WorldPackets.HandleRoutedPacket)
		self.registerWorldHandler(PacketHeader.ClientGameMessage.value, WorldPackets.HandleGameMessage)
		self.registerWorldHandler(PacketHeader.ClientPositionUpdate.value, WorldPackets.UpdateCharacterPositon)
		self.registerWorldHandler(PacketHeader.ClientLoadComplete.value, WorldPackets.HandleDetailedLoad)
		self.registerWorldHandler(PacketHeader.Handshake.value, WorldPackets.HandleHandshake)
		print("World Server Started")

		for Zone in ZoneNames:
			self.registerZone(Zone, SpawnLocation=DefaultZoneSpawns[Zone], lvlFiles=ZoneLvls[Zone])
		print("Finished Registering Zones!")

		updateThread = threading.Thread(target=self.updateLoop)
		updateThread.start()
		constructionThread = threading.Thread(target=self.constructionLoop)
		constructionThread.start()
		sleep(10)
		print("Server is Ready!")
	def handlePacket(self, data : bytes, address : Address):
		if(data[0:8] in self.WorldHandlers):
			t = threading.Thread(target=self.WorldHandlers[data[0:8]], args=[self, data[8:], address])
			t.start()
		else:
			print("Header {} Has No Handler!".format(data[0:8]))
	def registerReplicaManager(self, WorldID : int):
		self.ReplicaManagers[WorldID] = GameReplicaManager(self)
	def registerWorldHandler(self, header : PacketHeader, function : Callable):
		self.WorldHandlers[header] = function
	def registerZone(self, WorldID : int, lvlFiles : list, SpawnLocation : Vector3 = Vector3(0,0,0)):
		World = Zone(self.Game)
		World.ZoneID = WorldID
		World.SpawnLocation = SpawnLocation
		self.registerReplicaManager(WorldID)
		result = self.Game.registerZone(World, lvlFiles, self)
		if(result is not Exception): print("Registered '{}'".format(ZoneNames[WorldID]))

	def handleWorldDisconnect(self, address : Address):
		print("Got Disconnect From {}".format(address))
		game : GameManager = self.Game
		session : Session = game.getSessionByAddress(address)
		character : Character = game.getObjectByID(session.ObjectID)
		if(character is not None):
			zoneID = character.Zone
			if(session.State != SessionState.CharacterScreen and session.State != SessionState.LoggingIn and session.State is not None):
				self.ReplicaManagers[zoneID].remove_participant(address)
				self.ReplicaManagers[zoneID].destruct(character)
				del game.getZoneByID(zoneID).Objects[game.getZoneByID(zoneID).Objects.index(character)]
		del self.Game.Sessions[game.Sessions.index(session)]

	def constructionLoop(self):
		while True:
			for player in self.Game.getPlayers():
				session : Session = self.Game.getSessionByCharacterID(player.ObjectConfig["ObjectID"])
				RM: GameReplicaManager = self.ReplicaManagers[player.Zone]
				Zone = self.Game.getZoneByID(player.Zone)
				# GhostingDistance Loop
				for Object in Zone.Objects:
					if (isinstance(Object, ReplicaObject)):
						if (Object.ObjectConfig["ObjectID"] not in player.ClientObjects):
							if ((player.ObjectConfig["Position"].distance(Object.ObjectConfig["Position"]) < player.ObjectConfig[
								"GhostingDistance"] or Object.ObjectConfig["LOT"] == 1) and Object != player):
								player.ClientObjects.append(Object.ObjectConfig["ObjectID"])
								RM.construct(Object, recipients=[session.address])
								sleep(.05)
						else:
							if ((player.ObjectConfig["Position"].distance(Object.ObjectConfig["Position"]) > player.ObjectConfig[
								"GhostingDistance"] and Object != player) and Object.ObjectConfig["LOT"] != 1):
								try:
									player.ClientObjects.remove(Object.ObjectConfig["ObjectID"])
									RM.destruct(Object)
									sleep(.05)
								except:
									pass

	def updateLoop(self):
		while True:
			for player in self.Game.getPlayers():
				session : Session = self.Game.getSessionByCharacterID(player.ObjectConfig["ObjectID"])
				RM: GameReplicaManager = self.ReplicaManagers[player.Zone]
				if (RM.is_participant(session.address)):
					try:
						RM.serialize(player, recipients=[session.address])
					except:
						pass
					if((player.ObjectConfig["Health"] <= 0 or self.inKillElevation(player)) and "Unkillable" not in player.Tag.split(" ") and player.ObjectConfig["LoadingIn"] == False
					   and player.ObjectConfig["Alive"] == True):
						player.ObjectConfig["Alive"] = False
						player.ObjectConfig["Health"] = 0
						player.ObjectConfig["NeedsUpdate"] = True
						player.Kill(self)
					for ObjectID in player.ClientObjects:
						Object = self.Game.getObjectByID(ObjectID)
						if(isinstance(Object, ReplicaObject)):
							try:
								if((player.ObjectConfig["Position"].distance(Object.ObjectConfig["Position"]) < player.ObjectConfig["GhostingDistance"] and Object.ObjectConfig["NeedsUpdate"] == True) or Object == player):
										RM.serialize(Object, recipients=[session.address])
										Object.ObjectConfig["NeedsUpdate"] = False
							except:
								pass
						sleep(.0025)


	def inKillElevation(self, Player : Character):
		zone = Player.Zone
		yPos = Player.ObjectConfig["Position"].Y
		#TODO: Find death elevation for Ninjago
		if((zone == ZoneID.VentureExplorer or zone == ZoneID.ReturnToVentureExplorer) and yPos < 575):
			return True
		elif(zone == ZoneID.AvantGardens and yPos < 255):
			return True
		elif((zone == ZoneID.BlockYard or zone == ZoneID.AvantGrove or zone == ZoneID.NimbusRock or zone == ZoneID.ChanteyShantey or zone == ZoneID.RavenBluff) and yPos < 375):
			return True
		elif(zone == ZoneID.NimbusIsle and yPos < 445):
			return True
		elif(zone == ZoneID.GnarledForest and yPos < 165):
			return True
		elif(zone == ZoneID.CanyonCove and yPos < 210):
			return True
		elif(zone == ZoneID.ForbiddenValley and yPos < -60):
			return True
		elif(zone == ZoneID.Starbase3001 and yPos < 900):
			return True
		elif(zone == ZoneID.LEGOClub and yPos < 800):
			return True
		elif(zone == ZoneID.CruxPrime and yPos < -20):
			return True
		return False

	def OrientToObject(self, Object : ReplicaObject, Target : ReplicaObject):
		packet = WriteStream()
		self.InitializeGameMessage(packet, Object.ObjectConfig["ObjectID"], 0x0389)
		packet.write(c_longlong(Target.ObjectConfig["ObjectID"]))
		if(self.Game.getObjectZone(Object) is not None):
			self.brodcastPacket(packet, self.Game.getObjectZone(Object))

	def spawnObject(self, LOT : int, zoneID : ZoneID, CustomConfig : dict, Position : Vector3 = Vector3(0,0,0), Rotation : Vector4 = Vector4(0,0,0,0), debug : bool = True,
					initialize : bool = False):
		try:
			objectType = str(self.CDClient.Tables["Objects"].select(["type"], "id = {}".format(LOT))[0]["type"])
		except:
			return
		zone: Zone = self.Game.getZoneByID(zoneID)
		if(objectType == "Smashables"):
			gameObject = Smashable(zone)
			gameObject.ObjectConfig["LOT"] = LOT
			gameObject.ObjectConfig["Position"] = Position
			gameObject.ObjectConfig["Rotation"] = Rotation
			gameObject.ObjectConfig["ObjectType"] = "Smashables"
			for key in CustomConfig:
				gameObject.ObjectConfig[key] = CustomConfig[key]
			gameObject.setDestructible(self.CDClient)
		elif(objectType == "Enemies"):
			gameObject = Enemy(zone)
			gameObject.ObjectConfig["LOT"] = LOT
			gameObject.ObjectConfig["Position"] = Position
			gameObject.ObjectConfig["Rotation"] = Rotation
			gameObject.ObjectConfig["ObjectType"] = "Enemies"
			gameObject.setDestructible(self.CDClient)
		else:
			gameObject = ReplicaObject(zone)
			gameObject.ObjectConfig["LOT"] = LOT
			gameObject.ObjectConfig["Position"] = Position
			gameObject.ObjectConfig["Rotation"] = Rotation
			gameObject.ObjectConfig["ObjectType"] = objectType

		zone.createObject(gameObject)
		gameObject.Components = gameObject.findComponentsFromCDClient(self.CDClient)
		if (initialize == False):
			self.ReplicaManagers[zoneID].construct(gameObject)
		if(debug == True):
			print("Spawned Object with Type '{}' and LOT '{}'".format(objectType, LOT))

	def LoadWorld(self, Player: Character, zoneID: ZoneID, address: Address, SpawnAtDefault: bool = False):
		packet = WriteStream()
		print("Sending Player {} to {}".format(Player.ObjectConfig["ObjectID"], ZoneNames[zoneID]))
		writeHeader(packet, PacketHeader.WorldInfo)
		zone: Zone = self.Game.getZoneByID(zoneID)
		if(zoneID == 1000):
			Player.ObjectConfig["GhostingDistance"] = 500
		else:
			Player.ObjectConfig["GhostingDistance"] = 300
		packet.write(c_uint16(zoneID))
		packet.write(c_uint16(0))  # MapInstance
		packet.write(c_ulong(0))  # MapClone
		packet.write(c_ulong(ZoneChecksums[zoneID]))
		if (SpawnAtDefault):
			packet.write(c_float(zone.SpawnLocation.X))
			packet.write(c_float(zone.SpawnLocation.Y))
			packet.write(c_float(zone.SpawnLocation.Z))
			Player.ObjectConfig["Position"] = zone.SpawnLocation
		else:
			packet.write(c_float(Player.ObjectConfig["Position"].X))
			packet.write(c_float(Player.ObjectConfig["Position"].Y))
			packet.write(c_float(Player.ObjectConfig["Position"].Z))
		if (zone.ActivityWorld):
			packet.write(c_ulong(4))
		else:
			packet.write(c_ulong(0))
		session: Session = self.Game.getSessionByAddress(address)
		session.ZoneID = zoneID
		session.ObjectID = Player.ObjectConfig["ObjectID"]
		Player.ClientObjects = []
		Player.ObjectConfig["LoadingIn"] = True
		Player.Zone = zoneID
		for zone in self.ReplicaManagers:
			manager = self.ReplicaManagers[zone]
			if (manager.is_participant(address)):
				manager.remove_participant(address)
				manager.destruct(Player)
		RM: GameReplicaManager = self.ReplicaManagers[zoneID]
		RM.add_participant(address)
		self.send(packet, address)
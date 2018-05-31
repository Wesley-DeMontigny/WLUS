from typing import Callable
import WorldPackets
from PacketHeaders import PacketHeader
from Enum import ZoneID
from GameManager import GameManager, ReplicaObject, Humanoid, Character, Session
from GameDB import GameDB
import threading
from ServerUtilities import *
import pyraknet
from GameManager import Zone, Vector3
from pyraknet.replicamanager import *
from core import GameServer, GameReplicaManager
from time import sleep
import threading

class WorldServer(GameServer):
	def __init__(self, address: Address, max_connections: int, incoming_password: bytes, GameManager : GameManager, CDClient : GameDB):
		super().__init__(address, max_connections, incoming_password, GameManager, CDClient)
		self.add_handler(pyraknet.server.Event.UserPacket, self.handlePacket)
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
			self.registerZone(Zone, SpawnLocation=DefaultZoneSpawns[Zone])

		updateThread = threading.Thread(target=self.updateLoop)
		updateThread.start()
	def handlePacket(self, data : bytes, address):
		if(data[0:8] in self.WorldHandlers):
			t = threading.Thread(target=self.WorldHandlers[data[0:8]], args=[self, data[8:], address])
			t.start()
		else:
			print("Header {} Has No Handler!".format(data[0:8]))
	def registerReplicaManager(self, WorldID : int):
		self.ReplicaManagers[WorldID] = GameReplicaManager(self)
	def registerWorldHandler(self, header : PacketHeader, function : Callable):
		self.WorldHandlers[header] = function
	def registerZone(self, WorldID : int, lvlFiles : list = None, SpawnLocation : Vector3 = Vector3(0,0,0)):
		World = Zone(self.Game)
		World.ZoneID = WorldID
		World.SpawnLocation = SpawnLocation
		self.registerReplicaManager(WorldID)
		if(lvlFiles != None):
			"""Parse Lvl Files"""
		result = self.Game.registerZone(World)
		if(result is not Exception): print("Registered '{}'".format(ZoneNames[WorldID]))

	def updateLoop(self):
		while True:
			for Zone in self.Game.Zones:
				RM: GameReplicaManager = self.ReplicaManagers[Zone.ZoneID]
				for Object in Zone.Objects:
					if(isinstance(Object, ReplicaObject)):
						try:
							RM.serialize(Object)
						except:
							pass
					if(isinstance(Object, Character)):
						if((Object.ObjectConfig["Health"] <= 0 or self.inKillElevation(Object)) and "Unkillable" not in Object.Tag.split(" ")):
							if(Object.ObjectConfig["Alive"] == True):
								Object.ObjectConfig["Alive"] = False
								Object.ObjectConfig["Health"] = 0
								Object.Kill(self)
			sleep(1/3)

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
		elif(zone == ZoneID.ForbiddenValley and yPos < 60):
			return True
		elif(zone == ZoneID.Starbase3001 and yPos < 900):
			return True
		elif(zone == ZoneID.LEGOClub and yPos < 800):
			return True
		elif(zone == ZoneID.CruxPrime and yPos < -20):
			return True
		return False

	def LoadWorld(self, Player: Character, zoneID: ZoneID, address: Address, SpawnAtDefault: bool = False):
		packet = WriteStream()
		print("Sending Player {} to {}".format(Player.ObjectConfig["ObjectID"], ZoneNames[zoneID]))
		writeHeader(packet, PacketHeader.WorldInfo)
		zone: Zone = self.Game.getZoneByID(zoneID)
		packet.write(c_uint16(zoneID))
		packet.write(c_uint16(0))  # MapInstance
		packet.write(c_ulong(0))  # MapClone
		packet.write(c_ulong(ZoneChecksums[zoneID]))
		if (SpawnAtDefault or Player.ObjectConfig["Position"] == None):
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
		Player.Zone = zoneID
		for zone in self.ReplicaManagers:
			manager = self.ReplicaManagers[zone]
			if (manager.is_participant(address)):
				manager.remove_participant(address)
		RM: GameReplicaManager = self.ReplicaManagers[zoneID]
		RM.add_participant(address)
		self.send(packet, address)
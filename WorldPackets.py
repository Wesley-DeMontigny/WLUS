from ServerUtilities import *
from GameManager import *
from Enum import *
import time
from core import GameServer, GameReplicaManager
from structures import CString, Vector3
from AccountManager import Account
from xml.etree import ElementTree
from LDF import LDF
import zlib

def HandleHandshake(Server : GameServer, data : bytes, address : Address):
	stream = ReadStream(data)
	clientVersion = stream.read(c_ulong)

	Server.send(getHandshake(clientVersion, 4), address)

def HandleSessionKey(Server : GameServer, data : bytes, address : Address):
	stream = ReadStream(data)
	username = stream.read(str, allocated_length=33)
	userKey = stream.read(str, allocated_length=33)

	session = Server.Game.getSessionByAddress(address)
	if(session is not None and session.userKey == userKey and session.accountUsername == username):
		print(address, "sent the following valid key:", userKey)
		session.State = SessionState.CharacterScreen
	else:
		Server.send(getDisconnect(DisconnectionReasons.InvalidSessionKey.value), address)


def HandleMinifigListRequest(Server : GameServer, data : bytes, address : Address):
	session = Server.Game.getSessionByAddress(address)
	if(session.State == SessionState.CharacterScreen):
		characters = Server.Game.getAccountByUsername(session.accountUsername).Characters
		packet = WriteStream()
		writeHeader(packet, PacketHeader.MinifigureList)
		packet.write(c_uint8(len(characters)))
		packet.write(c_uint8(0))
		for character in characters:
			packet.write(c_longlong(character.ObjectConfig["ObjectID"]))#Object ID
			packet.write(c_ulong(0))
			packet.write(character.ObjectConfig["Name"], allocated_length=33)#Character Name
			packet.write("", allocated_length=33)#Name to show up in paranthesis
			packet.write(c_bool(False))#Name rejected
			packet.write(c_bool(False))#Free to play
			packet.write(CString("", allocated_length=10))#Unknown
			packet.write(c_ulong(character.ObjectConfig["ShirtColor"]))
			packet.write(c_ulong(character.ObjectConfig["ShirtStyle"]))
			packet.write(c_ulong(character.ObjectConfig["PantsColor"]))
			packet.write(c_ulong(character.ObjectConfig["HairStyle"]))
			packet.write(c_ulong(character.ObjectConfig["HairColor"]))
			packet.write(c_ulong(character.ObjectConfig["lh"]))
			packet.write(c_ulong(character.ObjectConfig["rh"]))
			packet.write(c_ulong(character.ObjectConfig["Eyebrows"]))
			packet.write(c_ulong(character.ObjectConfig["Eyes"]))
			packet.write(c_ulong(character.ObjectConfig["Mouth"]))
			packet.write(c_ulong(0))
			packet.write(c_uint16(character.Zone))
			packet.write(c_uint16(0))#MapInstance
			packet.write(c_ulong(0))#MapClone
			packet.write(c_ulonglong(0))
			equippedItems = character.ObjectConfig["Inventory"].getEquippedItems()
			packet.write(c_ushort(len(equippedItems)))
			for item in equippedItems:
				packet.write(c_ulong(item["LOT"]))
		Server.send(packet, address)

def HandleMinifigureCreation(Server : GameServer, data : bytes, address : Address):
	session : Session = Server.Game.getSessionByAddress(address)
	account : Account = Server.Game.getAccountByUsername(session.accountUsername)
	stream = ReadStream(data)
	name = stream.read(str, allocated_length=33)
	predefName1 = stream.read(c_ulong)
	predefName2 = stream.read(c_ulong)
	predefName3 = stream.read(c_ulong)
	stream.read(bytes, allocated_length=9)
	ShirtColor = stream.read(c_ulong)
	ShirtStyle = stream.read(c_ulong)
	PantsColor = stream.read(c_ulong)
	HairStyle = stream.read(c_ulong)
	HairColor = stream.read(c_ulong)
	lh = stream.read(c_ulong)
	rh = stream.read(c_ulong)
	Eyebrows = stream.read(c_ulong)
	Eyes = stream.read(c_ulong)
	Mouth = stream.read(c_ulong)
	account.CreateMinifigure(name, ShirtColor, ShirtStyle, PantsColor, HairColor, HairStyle, lh, rh, Eyebrows, Eyes, Mouth)
	time.sleep(.5)
	SendCreationResponse(Server, address, MinifigureCreationResponse.Success)
	HandleMinifigListRequest(Server, b"", address)

def HandleMinifigureDeletion(Server : GameServer, data : bytes, address : Address):
	stream = ReadStream(data)
	session : Session = Server.Game.getSessionByAddress(address)
	ObjectID = stream.read(c_longlong)
	account : Account = Server.Game.getAccountByUsername(session.accountUsername)
	for i in range(len(account.Characters)):
		if(account.Characters[i].ObjectConfig["ObjectID"] == ObjectID):
			del account.Characters[i]
			Server.ServerDB.Tables["Characters"].delete("ObjectID = {}".format(ObjectID))
			Server.ServerDB.Tables["CharacterStatistics"].delete("PlayerID = {}".format(ObjectID))
			Server.ServerDB.Tables["Inventory"].delete("OwnerID = {}".format(ObjectID))
			Server.ServerDB.Tables["CharacterConfig"].delete("PlayerID = {}".format(ObjectID))
			Server.ServerDB.Tables["CompletedMissions"].delete("PlayerID = {}".format(ObjectID))
			Server.ServerDB.Tables["CurrentMissions"].delete("PlayerID = {}".format(ObjectID))
			print("Deleted Character {}".format(ObjectID))
			return

def HandleJoinWorld(Server : GameServer, data : bytes, address : Address):
	stream = ReadStream(data)
	ObjectID = stream.read(c_longlong)
	player : Character = Server.Game.getCharacterByObjectID(ObjectID)
	if(player.Zone == ZoneID.NoZone.value):
		player.Zone = ZoneID.VentureExplorer.value
	SpawnAtDefault = False
	if(player.ObjectConfig["Position"].X < 2 and player.ObjectConfig["Position"].Y < 2 and player.ObjectConfig["Position"].Z < 2):
		SpawnAtDefault = True
	Server.LoadWorld(player, player.Zone, address, SpawnAtDefault=SpawnAtDefault)

def HandleGameMessage(Server : GameServer, data : bytes, address : Address):
	stream = ReadStream(data)
	objectID = stream.read(c_longlong)
	messageID = stream.read(c_ushort)
	object : GameObject = Server.Game.getObjectByID(objectID)
	if(object is not None):
		object.HandleEvent("GM_{}".format(str(hex(messageID).replace("x",""))), stream, address, Server)
	else:
		print("Object {} Does Not Exist!".format(objectID))


def HandleRoutedPacket(Server : GameServer, data : bytes, address : Address):
	""" TODO: Implement this """

def HandleDetailedLoad(Server : GameServer, data : bytes, address : Address):
	session : Session = Server.Game.getSessionByAddress(address)
	player : Character = Server.Game.getCharacterByObjectID(session.ObjectID)

	zone : Zone = Server.Game.getZoneByID(player.Zone)
	zone.createObject(player)

	ldf = LDF()
	ldf.registerKey("levelid", player.Zone, 1)
	ldf.registerKey("objid", player.ObjectConfig["ObjectID"], 9)
	ldf.registerKey("template", player.ObjectConfig["LOT"], 1)
	ldf.registerKey("name", player.ObjectConfig["Name"], 0)

	root = ElementTree.Element("obj")
	root.set("v", "1")
	buff = ElementTree.SubElement(root, "buff")
	skill = ElementTree.SubElement(root, "skill")

	inv = ElementTree.SubElement(root, "inv")
	bag = ElementTree.SubElement(inv, "bag")
	bagInfo = ElementTree.SubElement(bag, "b")
	bagInfo.set("t", "0")
	bagInfo.set("m", str(player.ObjectConfig["Inventory"].Space))
	items = ElementTree.SubElement(inv, "items")
	itemIn = ElementTree.SubElement(items, "in")
	for item in player.ObjectConfig["Inventory"].InventoryList:
		i = ElementTree.SubElement(itemIn, "i")
		i.set("l", str(item["LOT"]))
		i.set("id", str(item["ObjectID"]))
		i.set("s", str(item["Slot"]))
		i.set("c", str(item["Quantity"]))
		i.set("b", str(int(item["Linked"])))
		i.set("eq", str(int(item["Equipped"])))

	mf = ElementTree.SubElement(root, "mf")
	char = ElementTree.SubElement(root, "char")
	char.set("cc", str(player.ObjectConfig["Currency"]))
	char.set("ls", str(player.ObjectConfig["UniverseScore"]))
	lvl = ElementTree.SubElement(root, "lvl")
	lvl.set("l", str(player.ObjectConfig["Level"]))

	pets = ElementTree.SubElement(root, "pet")

	mis = ElementTree.SubElement(root, "mis")
	done = ElementTree.SubElement(mis, "done")
	for mission in player.ObjectConfig["CompletedMissions"]:
		m = ElementTree.SubElement(done, "m")
		m.set("id", str(mission))
		m.set("cct", "1")
		m.set("cts", "0")
	cur = ElementTree.SubElement(mis, "cur")
	for mission in player.ObjectConfig["CurrentMissions"]:
		m = ElementTree.SubElement(cur, "m")
		m.set("id", str(mission.MissionID))
		sv = ElementTree.SubElement(m, "sv")
		sv.set("v", str(mission.Progress))

	ldf.registerKey("xmlData", root, 13)

	LegoData = WriteStream()
	ldf.writeLDF(LegoData)
	ldfBytes = bytes(LegoData)
	compressed = zlib.compress(ldfBytes)

	packet = WriteStream()
	writeHeader(packet, PacketHeader.DetailedUserInfo)
	packet.write(c_ulong(len(compressed)+9))
	packet.write(c_bool(True))
	packet.write(c_ulong(len(ldfBytes)))
	packet.write(c_ulong(len(compressed)))
	packet.write(compressed)

	Server.send(packet, address)
	print("Sent Detailed User Info to Player {}".format(player.ObjectConfig["ObjectID"]))

	ConstructObjectsInZone(Server, address, zone.ZoneID, ExcludeIDs=[player.ObjectConfig["ObjectID"]])

	if (player.Components == []):
		player.Components = player.findComponentsFromCDClient(Server.CDClient)
	player.ObjectConfig["ObjectType"] = player.getObjectType(Server.CDClient)
	Server.ReplicaManagers[zone.ZoneID].construct(player)

	doneLoadingObjects = WriteStream()
	Server.InitializeGameMessage(doneLoadingObjects, player.ObjectConfig["ObjectID"], 0x066a)
	Server.send(doneLoadingObjects, address)

	playerReady = WriteStream()
	Server.InitializeGameMessage(playerReady, player.ObjectConfig["ObjectID"], 0x01fd)
	Server.send(playerReady, address)

def ConstructObjectsInZone(Server : GameServer, address : Address, zoneID : ZoneID, ExcludeIDs : list = None):
	zone : Zone = Server.Game.getZoneByID(zoneID)
	for Object in zone.Objects:
		if(isinstance(Object, ReplicaObject)):
			Object.ObjectConfig["ObjectType"] = Object.getObjectType(Server.CDClient)
			if(Object.Components == []):
				Object.Components = Object.findComponentsFromCDClient(Server.CDClient)
			if (Object.ObjectConfig["ObjectID"] not in ExcludeIDs):
				Server.ReplicaManagers[zoneID].construct(Object, recipients=[address])

def SendCreationResponse(Server : GameServer, address : Address, Response : MinifigureCreationResponse):
	packet = WriteStream()
	writeHeader(packet, PacketHeader.MinifigureCreationResponse)
	packet.write(c_uint8(Response.value))#Just going to leave it at success for now
	Server.send(packet, address)


def UpdateCharacterPositon(Server : GameServer, data : bytes, address : Address):
	stream = ReadStream(data)
	XPos = stream.read(c_float)
	YPos = stream.read(c_float)
	ZPos = stream.read(c_float)
	XRot = stream.read(c_float)
	YRot = stream.read(c_float)
	ZRot = stream.read(c_float)
	WRot = stream.read(c_float)
	session : Session = Server.Game.getSessionByAddress(address)
	character : Character = Server.Game.getObjectByID(session.ObjectID)
	character.ObjectConfig["Position"] = Vector3(XPos, YPos, ZPos)
	character.ObjectConfig["Rotation"] = Vector4(XRot, YRot, ZRot, WRot)
from ServerUtilities import *
from GameManager import *
from Enum import *
import time
from core import GameServer, CString

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
		Server.send(getDisconnect(DisconnectionReasons.InvalidSessionKey.value))

def HandleMinifigListRequest(Server : GameServer, data : bytes, address : Address):
	session = Server.Game.getSessionByAddress(address)
	if(session.State == SessionState.CharacterScreen):
		characters = Server.Game.getAccountByUsername(session.accountUsername).Characters
		packet = WriteStream()
		writeHeader(packet, PacketHeader.MinifigureList)
		packet.write(c_uint8(len(characters)))
		packet.write(c_uint8(0))
		for character in characters:
			packet.write(c_longlong(character.ObjectID))#Object ID
			packet.write(c_ulong(0))
			packet.write(character.Name, allocated_length=33)#Character Name
			packet.write("", allocated_length=33)#Name to show up in paranthesis
			packet.write(c_bool(False))#Name rejected
			packet.write(c_bool(False))#Free to play
			packet.write(CString("", allocated_length=10))#Unknown
			packet.write(c_ulong(character.ShirtColor))
			packet.write(c_ulong(character.ShirtStyle))
			packet.write(c_ulong(character.PantsColor))
			packet.write(c_ulong(character.HairStyle))
			packet.write(c_ulong(character.HairColor))
			packet.write(c_ulong(character.lh))
			packet.write(c_ulong(character.rh))
			packet.write(c_ulong(character.Eyebrows))
			packet.write(c_ulong(character.Eyes))
			packet.write(c_ulong(character.Mouth))
			packet.write(c_ulong(0))
			packet.write(c_uint16(character.Zone))
			packet.write(c_uint16(0))#MapInstance
			packet.write(c_ulong(0))#MapClone
			packet.write(c_ulonglong(0))
			equippedItems = character.Inventory.getEquippedItems()
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


def SendCreationResponse(Server : GameServer, address : Address, Response : MinifigureCreationResponse):
	packet = WriteStream()
	writeHeader(packet, PacketHeader.MinifigureCreationResponse)
	packet.write(c_uint8(Response.value))#Just going to leave it at success for now
	Server.send(packet, address)
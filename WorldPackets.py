from ServerUtilities import *
from GameManager import *

def HandleHandshake(Server : GameServer, data : bytes, address : Address):
	stream = ReadStream(data)
	clientVersion = stream.read(c_ulong)

	Server.send(getHandshake(clientVersion, 4), address)

def HandleSessionKey(Server : GameServer, data : bytes, address : Address):
	stream = ReadStream(data)
	username = stream.read(str, allocated_length=33)
	userKey = stream.read(str, allocated_length=33)

	session = Server.GameManager.getSessionByAddress(address)
	if(session is not None and session.userKey == userKey and session.accountUsername == username):
		print(address, "sent the following valid key:", userKey)
		session.State = SessionState.CharacterScreen
	else:
		Server.send(getDisconnect(DisconnectionReasons.InvalidSessionKey.value))

def HandleMinifigListRequest(Server : GameServer, data : bytes, address : Address):
	session = Server.GameManager.getSessionByAddress(address)
	if(session.State == SessionState.CharacterScreen):
		characters = Server.GameManager.ServerDB.Tables["Characters"].selectAll("AccountID = {}".format(session.accountID))
		packet = WriteStream()
		writeHeader(packet, PacketHeader.MinifigureList)
		packet.write(c_uint8(len(characters)))
		packet.write(c_uint8(0))
		for character in characters:
			print(character)
			packet.write(c_longlong(character["ObjectID"]))#Object ID
			packet.write(c_ulong(0))
			packet.write(character["Name"], allocated_length=33)#Character Name
			packet.write("", allocated_length=33)#Name to show up in paranthesis
			packet.write(c_bool(False))#Name rejected
			packet.write(c_bool(False))#Free to play
			packet.write(CString("", allocated_length=10))#Unknown
			packet.write(c_ulong(character["ShirtColor"]))
			packet.write(c_ulong(character["ShirtStyle"]))
			packet.write(c_ulong(character["PantsColor"]))
			packet.write(c_ulong(character["HairStyle"]))
			packet.write(c_ulong(character["HairColor"]))
			packet.write(c_ulong(character["lh"]))
			packet.write(c_ulong(character["rh"]))
			packet.write(c_ulong(character["Eyebrows"]))
			packet.write(c_ulong(character["Eyes"]))
			packet.write(c_ulong(character["Mouth"]))
			packet.write(c_ulong(0))
			packet.write(c_uint16(character["LastZone"]))
			packet.write(c_uint16(character["MapInstance"]))
			packet.write(c_ulong(character["MapClone"]))
			packet.write(c_ulonglong(0))
			packet.write(c_ushort(0))
		Server.send(packet, address)


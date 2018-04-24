import os
import threading
from threading import Thread
import asyncio
from messages import Message
import server
from bitstream import *
from socket import *
from Packet import *
from reliability import PacketReliability
import uuid
from struct import *
from replicamanager import *
from DBHandlers import *
from time import sleep
from GameMessage import *
from LDFReader import *
from ReplicaPacket import *
from LDFReader import *

class WorldServer(server.Server):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.register_handler(Message.LegoPacket, self.handleLegoPacket)
		self.register_handler(Message.NewIncomingConnection, self.addToParticipants)#Adds participant to replica manager
		self.Local = True
		self.SavedObjects = {}
		self.unhandledGMs = []
		self.RM = ReplicaManager(self)
		self.GM = GameMessages(self)
	def test(self):
		self.createObject("", 614, 547564808973508375, 1200, -40, 293.047, -16, 0, 0, 0, 0, Register=True)
	def offerMission(self, objectID, missionID, offererID):
		packet = self.GM.InitGameMessage(248, objectID)
		packet.write(c_int(missionID))
		packet.write(c_longlong(offererID))
		session = getSessionByCharacter(objectID)
		self.send(packet, (str(session[2]), int(session[7])))
	def orientToPosition(self, objectID, xPos, yPos, zPos):
		zone = getZoneOfObject(objectID)[0]
		packet = self.GM.InitGameMessage(906, objectID)
		packet.write(c_float(xPos))
		packet.write(c_float(yPos))
		packet.write(c_float(zPos))
		self.brodcastPacket(packet, int(zone))
	def orientToAngle(self, objectID, relativeToCurrent, angle):
		zone = getZoneOfObject(objectID)[0]
		packet = self.GM.InitGameMessage(906, objectID)
		packet.write(c_bit(relativeToCurrent))
		packet.write(c_float(angle))
		self.brodcastPacket(packet, int(zone))
	def brodcastPacket(self, packet, zoneID):
		connections = getConnectionsInZone(zoneID)
		for connection in connections:
			self.send(packet, (str(connection[0]), int(connection[1])))
	def SetJetPackMode(self, objectID, bypassChecks=False, doHover=False, Use=True, effectID=-1, airSpeed=10, maxAirSpeed=15, vertVel=1, warningEffectID=-1):
		zone = getZoneOfObject(objectID)[0]
		packet = self.GM.InitGameMessage(561, objectID)
		packet.write(c_bit(bypassChecks))
		packet.write(c_bit(doHover))
		packet.write(c_bit(Use))
		packet.write(c_int(effectID))
		packet.write(c_float(airSpeed))
		packet.write(c_float(maxAirSpeed))
		packet.write(c_float(vertVel))
		packet.write(c_int(warningEffectID))
		self.brodcastPacket(packet, int(zone))
	def createObject(self, Name, LOT, ObjectID, zone, xPos, yPos, zPos, xRot, yRot, zRot, wRot, RO=None, message=None, Register=True):
		if(RO != None):
			if(Register == True):
				registerWorldObject(Name, LOT, ObjectID, zone, xPos,yPos, zPos, xRot, yRot, zRot, wRot, self.RM._current_network_id)
			self.SavedObjects[ObjectID] = RO
			if(message == None):
				self.RM.construct(RO)
			else:
				self.RM.construct(RO, constructMsg=message)
		else:
			type = str(getObjectType(LOT)[0])
			if(type == "LEGO brick"):
				obj = BaseData()
				obj.objectID = c_longlong(ObjectID)
				obj.LOT = c_long(LOT)
				obj.NameLength = 0

				Physics = SimplePhysicsComponent()
				Physics.vectorFlag = True
				Physics.xPos = c_float(xPos)
				Physics.yPos = c_float(yPos)
				Physics.zPos = c_float(zPos)
				Physics.xRot = c_float(xRot)
				Physics.yRot = c_float(yRot)
				Physics.zRot = c_float(zRot)
				Physics.wRot = c_float(wRot)

				Render = RenderComponent()

				Object = ReplicaObject([obj, Physics, Render])
				if (Register == True):
					registerWorldObject(Name, LOT, ObjectID, zone, xPos, yPos, zPos, xRot, yRot, zRot, wRot, self.RM._current_network_id)
				self.SavedObjects[ObjectID] = Object
				if(message == None):
					self.RM.construct(Object)
				else:
					self.RM.construct(Object, constructMsg=message)
	def loadWorld(self, objectID, worldID, address, loadAtDefaultSpawn=False):
		deleteWorldObject(objectID)
		updateCharacterZone(worldID, objectID)  # Update session if needed
		characterData = getCharacterDataByID(objectID)  # Reload character data
		registerOrJoinWorld(worldID)
		# Register the world if there isn't one
		worldLoad = BitStream()
		# START OF HEADER
		worldLoad.write(c_ubyte(Message.LegoPacket))  # MSG ID ()
		worldLoad.write(c_ushort(0x05))  # Connection Type (UShort)
		worldLoad.write(c_ulong(0x02))  # Internal Packet ID (ULong)
		worldLoad.write(c_ubyte(0x00))  # Internal Packet ID (Uchar)
		###END OF HEADER
		worldLoad.write(c_ushort(int(worldID)))  # Write the last zone ID of the character
		worldLoad.write(c_ushort(0x00))  # Map instance
		worldLoad.write(c_ulong(0x00))  # Map clone
		checksum = Zones.zoneChecksums[(int(worldID))]
		for i in range(len(checksum)):
			worldLoad.write(c_ubyte(checksum[i]))  # Write special world checksum
		worldLoad.write(c_ushort(0x00))  # Unknown
		if (characterData[17] == None or characterData[18] == None or characterData[19] == None or loadAtDefaultSpawn == True):
			defaultSpawn = Zones.defaultZoneSpawns[(int(characterData[14]))]
			worldLoad.write(c_float(int(defaultSpawn[0])))  # Posx
			worldLoad.write(c_float(int(defaultSpawn[1])))  # Posy
			worldLoad.write(c_float(int(defaultSpawn[2])))  # Posz
			setCharacterPos(objectID, defaultSpawn[0], defaultSpawn[1], defaultSpawn[2])
		else:
			worldLoad.write(c_float(int(characterData[17])))  # Posx
			worldLoad.write(c_float(int(characterData[18])))  # Posy
			worldLoad.write(c_float(int(characterData[19])))  # Posz
		worldLoad.write(c_ulong(0x00))  # 0 if normal world. 4 if activity
		self.send(worldLoad, address, reliability=PacketReliability.ReliableOrdered)
	def addToParticipants(self, data, address):
		self.log("Just added new participant to replica manager")
		self.RM.add_participant(address)
	def handleLegoPacket(self, data, address):
		if(data[0:3] == bytearray(b'\x00\x00\x00')):#Handshake
			self.log("Lego Packet was Connection Init")
			handshake = BitStream()
			# START OF HEADER
			handshake.write(c_ubyte(Message.LegoPacket))  # MSG ID ()
			handshake.write(c_ushort(0x00))  # Connection Type (UShort)
			handshake.write(c_ulong(0x00))  # Internal Packet ID (ULong)
			handshake.write(c_ubyte(0x00))  # Internal Packet ID (Uchar)
			###END OF HEADER
			handshake.write(c_ulong(171022))  # Client version number
			handshake.write(c_ulong(0x93))  # Unknown, don't mess with it
			handshake.write(c_ulong(4))  # Remote Connection Type (1 for Auth, 4 for everything else)
			handshake.write(c_ulong(getpid()))  # Current PID
			handshake.write(c_short(-1))  # Unknown, speculated to be client port (0xff)
			handshake.write(str(socket.gethostbyname(socket.gethostname())))  # Local IP addr of server
			self.send(handshake, address, reliability=PacketReliability.ReliableOrdered)
		elif(data[0:3] == b"\x04\x00\x01"):
			self.log("Lego Packet was User Session Info")
			sessionInfo = getSessionByAddress(address[0])
			userRead = BitStream(data[7:])
			userIDRead = BitStream(data[73:])
			username = userRead.read(str)
			userID = userIDRead.read(str)
			self.log("Session Info - Username : " + str(username) + " UserKey : " + str(userID))
			if(sessionInfo[1] == getAccountByUsername(username)[0]):
				updateSessionByUserKey(userID, 1, "NULL", "NULL")
		elif(data[0:3] == b"\x04\x00\x02"):
			sleep(.5)
			session = getSessionByAddress(address[0])
			self.log("Lego Packet was Minifigure List Request")
			if(session[6] == 1):
				self.log("Client's Session is valid")
				rows, characterData = getCharacterData(session[1])
				if(rows > 4):
					rows = 4
				self.log("Account " + str(session[1]) + " has " + str(rows) + " character(s)")
				characterList = BitStream()
				# START OF HEADER
				characterList.write(c_ubyte(Message.LegoPacket))  # MSG ID ()
				characterList.write(c_ushort(0x05))  # Connection Type (UShort)
				characterList.write(c_ulong(0x06))  # Internal Packet ID (ULong)
				characterList.write(c_ubyte(0x00))  # Internal Packet ID (Uchar)
				###END OF HEADER
				characterList.write(c_ubyte(rows))#Number of characters
				characterList.write(c_ubyte(0x00))#Character to show up front
				for row in characterData:
					characterList.write(c_longlong(row[3]))#Object ID
					characterList.write(c_ulong(0x00))#Unknown, must be 0
					characterList.write(str(row[2]), allocated_length=66)#Name
					characterList.write("", allocated_length=66)
					characterList.write(c_byte(False))#Has custom name rejected
					characterList.write(c_byte(False))#Is free to play
					for _ in range(10):#Don't know what this stuff is for
						characterList.write_bits(b"\x00")
					characterList.write(c_ulong(row[4]))#Shirt color
					characterList.write(c_ulong(row[5]))#Shirt style
					characterList.write(c_ulong(row[6]))#Pants color
					characterList.write(c_ulong(row[8]))#Hair style
					characterList.write(c_ulong(row[7]))#Hair color
					characterList.write(c_ulong(row[9]))#lh??
					characterList.write(c_ulong(row[10]))#rh??
					characterList.write(c_ulong(row[11]))#Eyebrows
					characterList.write(c_ulong(row[12]))  # Eyes
					characterList.write(c_ulong(row[13]))  # Mouth
					characterList.write(c_ulong(0x00))#Unknown
					characterList.write(c_ushort(row[14]))  # Last Zone ID
					characterList.write(c_ushort(row[15]))  # map instance
					characterList.write(c_ulong(row[16]))  # map clone
					characterList.write(c_ulonglong(0x00))  # Last logout?
					items = getEquippedItems(str(row[3]))
					characterList.write(c_ushort(len(items)))#Equipped Item Lots
					for item in items:
						LOT = getLOTFromObject(str(item[0]))
						self.log("Found item in inventory with LOT " + str(LOT[0]))
						characterList.write_bits(c_ulong(int(LOT[0])))
				self.send(characterList, address, reliability=PacketReliability.ReliableOrdered)
			else:
				self.log("Client's Session is Invalid. Disconnecting...")
				DisconnectionNotify = BitStream()
				# START OF HEADER
				DisconnectionNotify.write(bytes(Message.LegoPacket))  # MSG ID
				DisconnectionNotify.write(bytes(0x00))  # Connection Type
				DisconnectionNotify.write(bytes(0x00))  # Internal Packet ID
				DisconnectionNotify.write(bytes(0x00))  # Unknown
				###END OF HEADER
				DisconnectionNotify.write(c_ulong(0x00))  # Unknown Server Error
				self.send(DisconnectionNotify, address)
				destroySessionWithAddress(address[0])
		elif(data[0:3] == b"\x04\x00\x03"):#When you create a minifigure you have to add a minfigure list packet
			self.log("Lego Packet was Minifigure Creation Request")
			session = getSessionByAddress(address[0])
			self.log("Lego Packet was Minifigure List Request")
			if(session[6] == 1):
				nameData = BitStream(data[7:])
				name = nameData.read(str)
				shirtColorData = BitStream(data[94:])
				shirtStyleData = BitStream(data[98:])
				pantsColorData = BitStream(data[102:])
				hairStyleData = BitStream(data[106:])
				hairColorData = BitStream(data[110:])
				lhData = BitStream(data[114:])
				rhData = BitStream(data[118:])
				eyebrowsData = BitStream(data[122:])
				eyesData = BitStream(data[126:])
				mouthData = BitStream(data[130:])
				shirtColor = shirtColorData.read(c_ulong)
				shirtStyle = shirtStyleData.read(c_ulong)
				pantsColor = pantsColorData.read(c_ulong)
				hairStyle = hairStyleData.read(c_ulong)
				hairColor = hairColorData.read(c_ulong)
				lh = lhData.read(c_ulong)
				rh = rhData.read(c_ulong)
				eyebrows = eyebrowsData.read(c_ulong)
				eyes = eyesData.read(c_ulong)
				mouth = mouthData.read(c_ulong)
				createMinifigure(session[1], name, shirtColor, shirtStyle, pantsColor,
								 hairStyle, hairColor, lh, rh, eyebrows, eyes, mouth)
				response = BitStream()
				# START OF HEADER
				response.write(c_ubyte(Message.LegoPacket))  # MSG ID ()
				response.write(c_ushort(0x05))  # Connection Type (UShort)
				response.write(c_ulong(0x07))  # Internal Packet ID (ULong)
				response.write(c_ubyte(0x00))  # Internal Packet ID (Uchar)
				###END OF HEADER
				response.write(c_ubyte(0x00))  # 0x00 is success
				self.send(response, address,reliability=PacketReliability.ReliableOrdered)  # Inform client character was created
				self.log("Client's Session is valid")
				rows, characterData = getCharacterData(session[1])
				if(rows > 4):
					rows = 4
				self.log("Account " + str(session[1]) + " now has " + str(rows) + " characters")
				characterList = BitStream()
				# START OF HEADER
				characterList.write(c_ubyte(Message.LegoPacket))  # MSG ID ()
				characterList.write(c_ushort(0x05))  # Connection Type (UShort)
				characterList.write(c_ulong(0x06))  # Internal Packet ID (ULong)
				characterList.write(c_ubyte(0x00))  # Internal Packet ID (Uchar)
				###END OF HEADER
				characterList.write(c_ubyte(rows))#Number of characters
				characterList.write(c_ubyte(0x00))#Character to show up front
				for row in characterData:
					characterList.write(c_longlong(row[3]))#Object ID
					characterList.write(c_ulong(0x00))#Unknown, must be 0
					characterList.write(str(row[2]), allocated_length=66)#Name
					characterList.write("", allocated_length=66)
					characterList.write(c_byte(False))#Has custom name rejected
					characterList.write(c_byte(False))#Is free to play
					for _ in range(10):#Don't know what this stuff is for
						characterList.write_bits(b"\x00")
					characterList.write(c_ulong(row[4]))#Shirt color
					characterList.write(c_ulong(row[5]))#Shirt style
					characterList.write(c_ulong(row[6]))#Pants color
					characterList.write(c_ulong(row[8]))#Hair style
					characterList.write(c_ulong(row[7]))#Hair color
					characterList.write(c_ulong(row[9]))#lh??
					characterList.write(c_ulong(row[10]))#rh??
					characterList.write(c_ulong(row[11]))#Eyebrows
					characterList.write(c_ulong(row[12]))  # Eyes
					characterList.write(c_ulong(row[13]))  # Mouth
					characterList.write(c_ulong(0x00))#Unknown
					characterList.write(c_ushort(row[14]))  # Last Zone ID
					characterList.write(c_ushort(row[15]))  # map instance
					characterList.write(c_ulong(row[16]))  # map clone
					characterList.write(c_ulonglong(0x00))  # Last logout?
					items = getEquippedItems(str(row[3]))
					characterList.write(c_ushort(len(items)))#Equipped Item Lots
					for item in items:
						LOT = getLOTFromObject(str(item[0]))
						self.log("Found item in inventory with LOT " + str(LOT[0]))
						characterList.write_bits(c_ulong(int(LOT[0])))
				self.send(characterList, address, reliability=PacketReliability.ReliableOrdered)
		elif(data[0:3] == b"\x04\x00\x06"):#Delete minifigure
			self.log("Lego Packet was Minifigure Deletion")
			objIdData = BitStream(data[7:])
			objId = objIdData.read(c_longlong)#Get objectID
			self.log("Deleting Minifigure with ID : " + str(objId))
			deleteCharacter(objId)#Delete It with the objID
		elif(data[0:3] == b"\x04\x00\x04"):#Character wants to enter world
			self.log("Lego Packet was World Enter Request")
			objectIDData = BitStream(data[7:])
			objectID = objectIDData.read(c_longlong)
			characterData = getCharacterDataByID(objectID)#Get character data
			if(characterData[14] == Zones.NO_ZONE):#If the character has no zone place him in venture explorer
				updateCharacterZone(Zones.VENTURE_EXPLORER, objectID)
			characterData = getCharacterDataByID(objectID)
			self.loadWorld(objectID, int(characterData[14]), address)
		elif(data[0:3] == b"\x04\x00\x13"):#Load character
			self.log("Lego Packet was Client Loading Complete")
			session = getSessionByAddress(address[0])
			characterData = getCharacterDataByID(session[4])
			zoneData = BitStream(data[7:])
			zoneID = zoneData.read(c_ushort)
			accountData = getAccountByAccountID(characterData[1])
			#START OF HEADER
			charHeader = BitStream()
			charHeader.write(c_ubyte(Message.LegoPacket))  # MSG ID
			charHeader.write(c_ushort(0x05))  # Connection Type (UShort)
			charHeader.write(c_ulong(0x04))  # Internal Packet ID (ULong)
			charHeader.write(c_ubyte(0x00))  # Internal Packet ID (Uchar)
			##END OF HEADER
			#Start of LDF
			LDF = BitStream()

			keyNumber = 0

			accountIDKeyAdj = BitStream()
			LDF.write(c_ubyte((b"accountID".__len__()*2)))
			accountIDKeyAdj.write("accountID", allocated_length=(b"accountID".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(accountIDKeyAdj[:-2])
			LDF.write(c_ubyte(8))  # Write data format 8
			LDF.write(c_int64(int(accountData[0])))#s64#Write int(characterData[1])
			keyNumber = keyNumber + 1

			chatmodeKeyAdj = BitStream()
			LDF.write(c_ubyte((b"chatmode".__len__() * 2)))
			chatmodeKeyAdj.write("chatmode", allocated_length=(b"chatmode".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(chatmodeKeyAdj[:-2])
			LDF.write(c_ubyte(1))  # Write data format 1
			LDF.write(c_int(int(accountData[4])))#Write int(accountData[4])
			keyNumber = keyNumber + 1

			editor_enabledKeyAdj = BitStream()
			LDF.write(c_ubyte((b"editor_enabled".__len__() * 2)))
			editor_enabledKeyAdj.write("editor_enabled", allocated_length=(b"editor_enabled".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(editor_enabledKeyAdj[:-2])
			LDF.write(c_ubyte(7))  # Write data format 7
			LDF.write(c_bool(False))#Write False?
			keyNumber = keyNumber + 1

			editor_levelKeyAdj = BitStream()
			LDF.write(c_ubyte((b"editor_level".__len__() * 2)))
			editor_levelKeyAdj.write("editor_level", allocated_length=(b"editor_level".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(editor_levelKeyAdj[:-2])
			LDF.write(c_ubyte(1))  # Write data format 1
			LDF.write(c_int(0))#Write 0?
			keyNumber = keyNumber + 1

			gmlevelKeyAdj = BitStream()
			LDF.write(c_ubyte((b"gmlevel".__len__() * 2)))
			gmlevelKeyAdj.write("gmlevel", allocated_length=(b"gmlevel".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(gmlevelKeyAdj[:-2])
			LDF.write(c_ubyte(1))  # Write data format 1
			LDF.write(c_int(int(0)))#Write int(accountData[4])
			keyNumber = keyNumber + 1

			levelidKeyAdj = BitStream()
			LDF.write(c_ubyte((b"levelid".__len__() * 2)))
			levelidKeyAdj.write("levelid", allocated_length=(b"levelid".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(levelidKeyAdj[:-2])
			LDF.write(c_ubyte(8))  # Write data format 8
			LDF.write(c_int64(zoneID))#s64#Write int(zoneID)
			keyNumber = keyNumber + 1

			objidKeyAdj = BitStream()
			LDF.write(c_ubyte((b"objid".__len__() * 2)))
			objidKeyAdj.write("objid", allocated_length=(b"objid".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(objidKeyAdj[:-2])#Remove 2 unnecessary bits
			LDF.write(c_ubyte(9))  # Write data format 9
			LDF.write(c_int64(int(characterData[3])))#Write int(characterData[3])
			keyNumber = keyNumber + 1

			reputationKeyAdj = BitStream()
			LDF.write(c_ubyte((b"reputation".__len__() * 2)))
			reputationKeyAdj.write("reputation", allocated_length=(b"reputation".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(reputationKeyAdj[:-2])
			LDF.write(c_ubyte(8))  # Write data format 8
			LDF.write(c_int64(100))#s64#Write 100
			keyNumber = keyNumber + 1

			templateKeyAdj = BitStream()
			LDF.write(c_ubyte((b"template".__len__() * 2)))
			templateKeyAdj.write("template", allocated_length=(b"template".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(templateKeyAdj[:-2])#Remove 2 unnecessary bits
			LDF.write(c_ubyte(1))  # Write data format 1
			LDF.write(c_int(1))#Write 1
			keyNumber = keyNumber + 1 #Update key number


			xml = '<?xml version="1.0"?><obj v="1"><buff/><skill/>'#Basic start of xml
			xml = xml + '<inv><bag><b t="0" m="'+str(characterData[24])+'"/></bag>'#Inventory bag space
			xml = xml + '<items><in>'#Items in inventory setup
			LOT, OBJECT, QUANTITY, LINKED, SPAWNERID, SLOT = getInventoryInfo(characterData[3])
			for i in range(len(LOT)):#Add all the items in inventory
				baseItem = '<i l="'+str(LOT[i][0])+'" id ="'+str(OBJECT[i])+'" s="'+str(SLOT[i])+'"'
				if(QUANTITY[i] > 1):
					baseItem =  baseItem + ' c="'+str(QUANTITY[i])+'"'
				if(SPAWNERID[i] != None):
					if(SPAWNERID > -1):
						baseItem = baseItem + ' sk="'+str(SPAWNERID[i])+'"'
				if(LINKED[i] == 1):
					baseItem = baseItem + ' b="1"'
				if(SPAWNERID[i] != None):
					if(SPAWNERID > -1):
						#Do rocket stuff here
						self.log("Spawner ids are not implemented yet")#A simple implementation can probably be found in the LUNI file WorldConnection.cpp
				baseItem = baseItem + '/>'
				xml = xml + baseItem
			xml = xml + '</in></items></inv>'#Close inventory
			xml = xml + '<mf/><char cc="'+str(characterData[21])+'"></char>'#Currency
			xml = xml + '<lvl l="'+str(characterData[20])+'"/><flag/><pet/>'#Level and flag and pet
			completedMissions = getCompletedMissions(characterData[3])
			if(completedMissions != None):#If there are completed missions write them to the xml
				missionData = '<mis><done>'
				for mission in completedMissions:
					missionData = missionData + '<m id="'+str(mission[0])+'" cts="0" cct="1"/>'
				missionData = missionData + "</done></mis>"
				xml = xml + missionData
			else:
				xml = xml + '</mis>'#If there are no missions write nothing
			xml = xml + "<mnt/><dest/></obj>"#Idk what these three are. Should probably find that out

			xmlKeyAdj = BitStream()
			LDF.write(c_ubyte((b"xmlData".__len__() * 2)))
			xmlKeyAdj.write("xmlData", allocated_length=(b"xmlData".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(xmlKeyAdj[:-2])
			LDF.write(c_ubyte(13))  # Write data format
			LDF.write(c_ulong((xml.__len__()+1))) # xml length
			LDF.write(xml, allocated_length=(len(xml)+1), char_size=1)  # xml data
			keyNumber = keyNumber + 1

			nameKeyAdj = BitStream()
			LDF.write(c_ubyte((b"name".__len__() * 2)))
			nameKeyAdj.write("name", allocated_length=(b"name".__len__()*2)+2)  # Write encoded key as bits
			LDF.write(nameKeyAdj[:-2])
			LDF.write(c_ubyte(0))  # Write data format 0
			LDF.write(c_uint((str(characterData[2]).__len__()*2)+2))#Write String Length
			LDF.write(str(characterData[2]), allocated_length=(str(characterData[2]).__len__()*2)+2)  # String
			keyNumber = keyNumber + 1

			adjLDF = BitStream()#Create Final LDF Stream
			adjLDF.write(c_uint(keyNumber))#Add Key Number
			adjLDF.write(LDF)#Add LDF

			Bitsize = len(adjLDF) + 5  # Adjust for the ulong and bool
			finalPacket = BitStream()  # Create new packet
			finalPacket.write_bits(charHeader)  # Write the header
			finalPacket.write(c_ulong(Bitsize))  # The size of the following data including the bool and ulong
			finalPacket.write(c_bool(False))  # Is compressed. LUNI has it set to false so I'll leave it there.

			finalPacket.write(adjLDF)  # Writes all the LDF data

			self.send(finalPacket, address, reliability=PacketReliability.ReliableOrdered)

			self.log("Sent Detailed User Info")

			objects = getObjectsInZone(zoneID)
			for obj in objects:
				self.createObject(obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7], obj[8], obj[9], obj[10], obj[11], Register=False, message="Sent World Object " + str(obj[3]))

			#Add Base Data
			Player = BaseData()
			Player.objectID = c_int64(int(characterData[3]))
			Player.LOT = c_long(1)
			Player.flag6 = True
			Player.NameLength = (str(characterData[2]).__len__())
			Player.Name = str(characterData[2])

			#Add Controllable Physics
			ControllablePhysics = ControllablePhysicsComponent()
			ControllablePhysics.flag2 = True
			ControllablePhysics.flag4 = True
			ControllablePhysics.vectorFlag = True
			ControllablePhysics.xPos = c_float(int(characterData[17]))
			ControllablePhysics.yPos = c_float(int(characterData[18]))
			ControllablePhysics.zPos = c_float(int(characterData[19]))
			ControllablePhysics.xRot = c_float(0.0)
			ControllablePhysics.yRot = c_float(0.0)
			ControllablePhysics.zRot = c_float(0.0)
			ControllablePhysics.wRot = c_float(0.0)
			ControllablePhysics.onGround=True


			#Add Destructible
			Destructible = DestructibleIndex()
			Destructible.flag1 = False

			#Add Stats
			Stats = StatsIndex()
			Stats.flag1 = True
			Stats.currentHealth = c_ulong(4)
			Stats.maxHealth = c_float(4)
			Stats.currentArmor = c_ulong(0)
			Stats.maxArmor = c_float(0)
			Stats.currentImagination = c_ulong(0)
			Stats.maxImagination = c_float(0)
			Stats.flag2 = True

			#Add Character Component
			Character = CharacterComponent()
			Character.hasLevel = True
			Character.level = c_ulong(characterData[20])
			info = PlayerInfo()
			info.setInfo(characterData[3])
			Character.info = info
			style = PlayerStyle()
			style.setStyle(characterData[3])
			Character.style = style
			data9 = Component4_Data9()
			Character.data9 = data9
			data11 = Component4_Data11()
			Character.data11 = data11

			#Add Inventory
			Inventory = InventoryComponent()
			Inventory.flag1 = True
			Inventory.characterObjID = characterData[3]

			#Add Script
			Script = ScriptComponent()

			#Add Skill
			Skill = SkillComponent()

			#Add Render
			Render = RenderComponent()

			#Add Component 107
			Comp107 = Component107()
			Comp107.flag1 = True

			PlayerComponents = [Player, ControllablePhysics, Destructible, Stats, Character, Inventory, Script, Skill, Render, Comp107]
			player = ReplicaObject(PlayerComponents)
			self.createObject(characterData[2], 1, int(characterData[3]), zoneID, int(characterData[17]), int(characterData[18]), int(characterData[19]), 0.0, 0.0, 0.0, 0.0, RO=player, message="Sent Player Construction")

			self.GM.SendGameMessage(1642, int(characterData[3]), address)#Server done loading all objects
			self.GM.SendGameMessage(509, int(characterData[3]), address)  # Player ready?

		elif(data[0:3] == b"\x04\x00\x05"):
			message = BitStream(data[7:])
			objID = message.read(c_longlong)
			msgID = message.read(c_ushort)
			if(str(msgID) == "1485"):
				self.log("Message was defined as 'Modify Ghosting Distance'")
			elif(str(msgID) == "41"):
				self.log("Message was defined as 'Play Emote'")
				emoteID = message.read(c_int)
				targetID = message.read(c_longlong)
				self.log("Emote ID:" + str(emoteID) + ", Target ID: " + str(targetID))
			elif(str(msgID) == "505"):
				playerID = message.read(c_longlong)
				self.log("Player with ID: " + str(playerID) + " has loaded")
			elif(str(msgID) == "888"):
				objectID = message.read(c_longlong)
				self.log("Object " + str(objectID) + " needs an update")
				# Components = self.SavedObjects[objectID].components
				# #If Object is a player
				# if(Components[0].LOT == c_long(1)):
				# 	Object = ReplicaObject(Components)
			elif(str(msgID) == "767"):
				#ToggleGhostReferenceOveride
				bit = message.read(c_bit)
				self.log("Ghost Reference Overide Gave Bit: " + str(bit))
			elif(str(msgID) == "768"):
				#SetGhostReferencePosition
				xPos = message.read(c_float)
				yPos = message.read(c_float)
				zPos = message.read(c_float)
			elif(str(msgID) == "124"):
				#SelectSkill
				fromSkillSet = message.read(c_bit)
				skillID = message.read(c_long)
				self.log("Select Skill " + str(skillID))
			elif(str(msgID) == "1202"):
				self.log("Player Was Smashed")
			else:
				self.log("Message id of "+ str(msgID) +" currently has no handler and is not defined!")
				self.unhandledGMs.append((msgID, objID))
		elif(data[0:3] == b"\x04\x00\x15"):
			#This needs to be figured out how to implement
			self.log("Lego Packet was 'Some Kind of Indicator This Packet Should Be Routed'????")
			#self.log(data[11:])
		elif(data[0:3] == b"\x04\x00\x16"):
			#self.log("[" + self.role + "]" + "Lego Packet was Position/Rotation Update")
			#session = getSessionByAddress(address[0])
			info = BitStream(data[7:])
			posX = info.read(c_float)
			posY = info.read(c_float)
			posZ = info.read(c_float)
			rotX = info.read(c_float)
			rotY = info.read(c_float)
			rotZ = info.read(c_float)
			rotW = info.read(c_float)
			#updateWorldObject(session[4], posX, posY, posZ, rotX, rotY, rotZ, rotW)

		else:
			self.log("Received Unknown Packet:")
			self.log(data)
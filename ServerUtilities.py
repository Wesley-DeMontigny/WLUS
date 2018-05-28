from pyraknet.bitstream import *
from PacketHeaders import PacketHeader
import os
import socket
from Enum import *

"""
This entire file is really just Misc functions and classes
"""

#Returns shirt lots needed for minifigure creation
def getShirtID(shirtColor : int, shirtStyle : int):
	shirtID = 0

	if(shirtColor == 0):
		if(shirtStyle >= 35):
			shirtID = 5730
		else:
			shirtID = ClothingLOT.SHIRT_BRIGHT_RED.value
	elif(shirtColor == 1):
		if(shirtStyle >= 35):
			shirtID = 5736
		else:
			shirtID = ClothingLOT.SHIRT_BRIGHT_BLUE.value
	elif (shirtColor == 3):
		if(shirtStyle >= 35):
			shirtID = 5808
		else:
			shirtID = ClothingLOT.SHIRT_DARK_GREEN.value
	elif (shirtColor == 5):
		if(shirtStyle >= 35):
			shirtID = 5754
		else:
			shirtID = ClothingLOT.SHIRT_BRIGHT_ORANGE.value
	elif (shirtColor == 6):
		if(shirtStyle >= 35):
			shirtID = 5760
		else:
			shirtID = ClothingLOT.SHIRT_BLACK.value
	elif (shirtColor == 7):
		if(shirtStyle >= 35):
			shirtID = 5766
		else:
			shirtID = ClothingLOT.SHIRT_DARK_STONE_GRAY.value
	elif (shirtColor == 8):
		if(shirtStyle >= 35):
			shirtID = 5772
		else:
			shirtID = ClothingLOT.SHIRT_MEDIUM_STONE_GRAY.value
	elif (shirtColor == 9):
		if(shirtStyle >= 35):
			shirtID = 5778
		else:
			shirtID = ClothingLOT.SHIRT_REDDISH_BROWN.value
	elif (shirtColor == 10):
		if(shirtStyle >= 35):
			shirtID = 5784
		else:
			shirtID = ClothingLOT.SHIRT_WHITE.value
	elif (shirtColor == 11):
		if(shirtStyle >= 35):
			shirtID = 5802
		else:
			shirtID = ClothingLOT.SHIRT_MEDIUM_BLUE.value
	elif (shirtColor == 13):
		if(shirtStyle >= 35):
			shirtID = 5796
		else:
			shirtID = ClothingLOT.SHIRT_DARK_RED.value
	elif (shirtColor == 14):
		if(shirtStyle >= 35):
			shirtID = 5802
		else:
			shirtID = ClothingLOT.SHIRT_EARTH_BLUE.value
	elif (shirtColor == 15):
		if(shirtStyle >= 35):
			shirtID = 5808
		else:
			shirtID = ClothingLOT.SHIRT_EARTH_GREEN.value
	elif (shirtColor == 16):
		if(shirtStyle >= 35):
			shirtID = 5814
		else:
			shirtID = ClothingLOT.SHIRT_BRICK_YELLOW.value
	elif (shirtColor == 84):
		if(shirtStyle >= 35):
			shirtID = 5820
		else:
			shirtID = ClothingLOT.SHIRT_SAND_BLUE.value
	elif (shirtColor == 96):
		if(shirtStyle >= 35):
			shirtID = 5826
		else:
			shirtID = ClothingLOT.SHIRT_SAND_GREEN.value

	editedShirtColor = shirtID

	if(shirtStyle >= 35):
		finalShirtID = editedShirtColor + (shirtStyle - 35)
	else:
		finalShirtID = editedShirtColor + (shirtStyle - 1)

	return finalShirtID

#Returns pants LOTS needed for minifigure creation
def getPantsID(pantsColor : int):
	if(pantsColor == 0):
		return ClothingLOT.PANTS_BRIGHT_RED.value
	elif(pantsColor == 1):
		return ClothingLOT.PANTS_BRIGHT_BLUE.value
	elif(pantsColor == 3):
		return ClothingLOT.PANTS_DARK_GREEN.value
	elif(pantsColor == 5):
		return ClothingLOT.PANTS_BRIGHT_ORANGE.value
	elif(pantsColor == 6):
		return ClothingLOT.PANTS_BLACK.value
	elif(pantsColor == 7):
		return ClothingLOT.PANTS_DARK_STONE_GRAY.value
	elif(pantsColor == 8):
		return ClothingLOT.PANTS_MEDIUM_STONE_GRAY.value
	elif(pantsColor == 9):
		return ClothingLOT.PANTS_REDDISH_BROWN.value
	elif(pantsColor == 10):
		return ClothingLOT.PANTS_WHITE.value
	elif(pantsColor == 11):
		return ClothingLOT.PANTS_MEDIUM_BLUE.value
	elif(pantsColor == 13):
		return ClothingLOT.PANTS_DARK_RED.value
	elif(pantsColor == 14):
		return ClothingLOT.PANTS_EARTH_BLUE.value
	elif(pantsColor == 15):
		return ClothingLOT.PANTS_EARTH_GREEN.value
	elif(pantsColor == 16):
		return ClothingLOT.PANTS_BRICK_YELLOW.value
	elif(pantsColor == 84):
		return ClothingLOT.PANTS_SAND_BLUE.value
	elif(pantsColor == 96):
		return ClothingLOT.PANTS_SAND_GREEN.value
	else:
		return 2508


#This is used to write standard packet headers
def writeHeader(Stream : WriteStream, Header : PacketHeader):
	Stream.write(Header.value)


def getHandshake(ClientVersion : int, ConnectionType : int):
	packet = WriteStream()

	writeHeader(packet, PacketHeader.Handshake)

	packet.write(c_ulong(ClientVersion))
	packet.write(c_ulong(0x93))
	packet.write(c_ulong(ConnectionType))#Connection Type (1 For Auth, 4 For Everything Else)
	packet.write(c_ulong(os.getpid()))
	packet.write(c_short(0xff))#Local port
	packet.write(str(socket.gethostbyname(socket.gethostname())), allocated_length=33)

	return packet

def getDisconnect(Reason : int):
	packet = WriteStream()
	writeHeader(packet, PacketHeader.DisconnectNotify)
	packet.write(c_ulong(Reason))
	return packet
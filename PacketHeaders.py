from enum import Enum
from pyraknet.bitstream import *


def generateHeaderFromList(HeaderList : list):
	stream = WriteStream()
	for i in HeaderList:
		stream.write(i)
	return stream.__bytes__()

class PacketHeader(Enum):
	Handshake = b'S\x00\x00\x00\x00\x00\x00\x00'
	DisconnectNotify = b"S\x00\x00\x01\x00\x00\x00\x00"
	ClientLoginInfo = b'S\x01\x00\x00\x00\x00\x00\x00'
	LoginResponse = b'S\x05\x00\x00\x00\x00\x00\x00'
	ClientUserSessionInfo = b"S\x04\x00\x01\x00\x00\x00\x00"
	ClientMinifigureListRequest = b"S\x04\x00\x02\x00\x00\x00\x00"
	MinifigureList = b"S\x05\x00\x06\x00\x00\x00\x00"

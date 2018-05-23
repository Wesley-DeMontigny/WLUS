from pyraknet.bitstream import *
from PacketHeaders import PacketHeader
import os
import socket
import pyraknet.server as Server
from GameManager import GameManager
from pyraknet.messages import Address
from enum import IntEnum

class GameServer(Server.Server):
	def __init__(self, address: Address, max_connections: int, incoming_password: bytes, GameManager : GameManager):
		super().__init__(address, max_connections, incoming_password)
		self.GameManager = GameManager

#This is used to write standard packet headers
def writeHeader(Stream : WriteStream, Header : PacketHeader):
	Stream.write(Header.value)

#Ripped this straight off of PYLUS Because I had no idea how to make the char_size of strings equal to 1. Idk why it was removed as a parameter but whatever I guess
class CString(Serializable):
	def __init__(self, data='', allocated_length=None, length_type=None):
		self.data = data
		self.allocated_length = allocated_length
		self.length_type = length_type

	def serialize(self, stream):
		stream.write(self.data if isinstance(self.data, bytes) else bytes(self.data, 'latin1'),
					 allocated_length=self.allocated_length, length_type=self.length_type)

	def deserialize(self, stream):
		return stream.read(bytes, allocated_length=self.allocated_length, length_type=self.length_type).decode('latin1')

class DisconnectionReasons(IntEnum):
	UnknownError = 0x00
	DuplicateLogin = 0x04
	ServerShutdown = 0x05
	ServerCannotLoadMap = 0x06
	InvalidSessionKey = 0x07
	CharacterNotFound = 0x09
	CharacterCorruption = 0x0a
	Kicked = 0x0b

class LoginResponseEnum(IntEnum):
	Success = 0x01
	Banned = 0x02
	InvalidPerm = 0x03
	InvalidLoginInfo = 0x06
	AccountLocked = 0x07

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
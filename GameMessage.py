from bitstream import *
import server
import replicamanager
from messages import *


class GameMessages:
	def __init__(self, server):
		self.server = server
		self.customMessageHandlers =[]
	def registerHandler(self, msg, function):
		self.customMessageHandlers.append((msg, function))
	def InitGameMessage(self, msg, objID):
		packet = BitStream()
		packet.write(c_ubyte(Message.LegoPacket))  # MSG ID ()
		packet.write(c_ushort(0x05))  # Connection Type (UShort)
		packet.write(c_ulong(0x0c))  # Internal Packet ID (ULong)
		packet.write(c_ubyte(0x00))  # Internal Packet ID (Uchar)
		packet.write(c_longlong(objID))#Target object ID
		packet.write(c_ushort(msg))
		return packet
	def SendGameMessage(self, msg, objID, address, additionalData=None):
		print("[" + self.server.role + "]" + "Sent game msg " + str(msg))
		if(additionalData == None):
			self.server.send(self.InitGameMessage(msg, objID), address)
		else:
			GM = BitStream()
			GM.write(c_ubyte(Message.LegoPacket))  # MSG ID ()
			GM.write(c_ushort(0x05))  # Connection Type (UShort)
			GM.write(c_ulong(0x0c))  # Internal Packet ID (ULong)
			GM.write(c_ubyte(0x00))  # Internal Packet ID (Uchar)
			GM.write(c_longlong(objID))  # Target object ID
			GM.write(c_ushort(msg))
			GM.write(additionalData)
			self.server.send(GM, address)


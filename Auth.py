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
from replicamanager import *
from DBHandlers import *
from time import sleep
from GameMessage import *
from LDFReader import *
from ReplicaPacket import *

class AuthServer(server.Server):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.register_handler(Message.LegoPacket, self.handleLegoPacket)
		self.Local = True
	def handleLegoPacket(self, data, address):
		serverIPPlugIn = socket.gethostbyname(socket.gethostname())
		if(self.Local == True):
			serverIPPlugIn = "127.0.0.1"
		serverIP = str(serverIPPlugIn).encode("UTF-8")
		for _ in range(33 - len(serverIP)):
			serverIP = serverIP + b"\x00"
		if(data[0:3] == bytearray(b'\x00\x00\x00')):
			print("["+self.role+"]"+"Lego Packet was Connection Init")
			handshake = BitStream()
			# START OF HEADER
			handshake.write(c_ubyte(Message.LegoPacket))  # MSG ID ()
			handshake.write(c_ushort(0x00))  # Connection Type (UShort)
			handshake.write(c_ulong(0x00))  # Internal Packet ID (ULong)
			handshake.write(c_ubyte(0x00))  # Internal Packet ID (Uchar)
			###END OF HEADER
			handshake.write(c_ulong(171022))  # Client version number
			handshake.write(c_ulong(0x93))  # Unknown, don't mess with it
			handshake.write(c_ulong(1))  # Remote Connection Type (1 for Auth, 4 for everything else)
			handshake.write(c_ulong(getpid()))  # Current PID
			handshake.write(c_short(-1))  # Unknown, speculated to be client port (0xff)
			handshake.write(str(socket.gethostbyname(socket.gethostname())))  # Local IP addr of server
			self.send(handshake, address, reliability=PacketReliability.ReliableOrdered)
		elif(data[0:3] == bytearray(b'\x01\x00\x00')):
			print("["+self.role+"]"+"Lego Packet was Login Info")
			userRead = BitStream(data[7:])#Displace the 7 bit header
			passwordRead = BitStream(data[73:])#Add 66 bits to the already 7 bit displacement
			username = (userRead.read(str)).replace(" ", "")
			password = passwordRead.read(str, allocated_length=41)
			print("["+self.role+"]"+"Login Username:" + username)#Length is 66 so divide it by 2 becuase its a wstring
			print("["+self.role+"]"+"Login Password:" + password)#Length is 82 so divide it by 2 becuase its a wstring
			loginResponse = getLoginResponse(username, password)
			loginData = BitStream()
			# START OF HEADER
			loginData.write(c_ubyte(Message.LegoPacket))  # MSG ID ()
			loginData.write(c_ushort(0x05))  # Connection Type (UShort)
			loginData.write(c_ulong(0x00))  # Internal Packet ID (ULong)
			loginData.write(c_ubyte(0x00))  # Internal Packet ID (Uchar)
			###END OF HEADER
			loginData.write(c_ubyte(loginResponse))#Response code (0x01 = Success, 0x06 = Invalid Login Info, 0x00 or 0x04 = Failed to login, 0x05 = Custom Msg)
			talkLikeAPirate_Len = len(b"\x54\x61\x6c\x6b\x5f\x4c\x69\x6b\x65\x5f\x41\x5f\x50\x69\x72\x61\x74\x65")#Talk_Like_A_Pirate Length
			talkLikeAPirate = b"\x54\x61\x6c\x6b\x5f\x4c\x69\x6b\x65\x5f\x41\x5f\x50\x69\x72\x61\x74\x65"#Talk like a pirate
			for _ in range(33 - talkLikeAPirate_Len):#For some dumb reason the normal write function thinks the string is too long so I just wrote it in bits
				talkLikeAPirate = talkLikeAPirate + b"\x00"
			loginData.write_bits(talkLikeAPirate)#Required for login. Not sure why it is what it is
			for _ in range(7):
				for _ in range(33):#There is space for 7 empty strings here... Don't know why
					loginData.write_bits(b"\x00")
			loginData.write(c_ushort(1))
			loginData.write(c_ushort(10))#These three are client version stuff
			loginData.write(c_ushort(64))
			userkey = (str(uuid.uuid4())[0:8])
			loginData.write(userkey, allocated_length=66)#Generated user key
			loginData.write_bits(serverIP)#IP redirect to character instance (I guess the world will handle it)
			loginData.write_bits(serverIP)#IP of chat sever
			loginData.write(c_ushort(2002))#World server port
			loginData.write(c_ushort(3003))#Chat server port
			loginData.write_bits(serverIP)#IP of something else, not sure. Docs says it might be an alternate redirect
			guid = b"00000000-0000-0000-0000-000000000000"
			for _ in range(37 - len(guid)):
				guid = guid + b"\x00"
			loginData.write_bits(guid)#Some kind of guid. It is always this value?
			loginData.write(c_ulong(0))#Always zero
			#Localization(3 bytes)
			loginData.write_bits(b"\x55\x53\x00")
			###End of Localization
			loginData.write(c_bit(False))#If it is user's first time logging in
			loginData.write(c_bit(True))#Free to play
			loginData.write(c_longlong(0x00))#Length of custom error msg
			#A whole lotta stamp stuff that I really don't get...
			bitStream = [loginData]
			bitStream[0].write(c_ulong(320))
			self.CreateExtraPacketData(0, 0, 2803442767, bitStream)
			self.CreateExtraPacketData(7, 37381, 2803442767, bitStream)
			self.CreateExtraPacketData(8, 6, 2803442767, bitStream)
			self.CreateExtraPacketData(9, 0, 2803442767, bitStream)
			self.CreateExtraPacketData(10, 0, 2803442767, bitStream)
			self.CreateExtraPacketData(11, 1, 2803442767, bitStream)
			self.CreateExtraPacketData(14, 1, 2803442767, bitStream)
			self.CreateExtraPacketData(15, 0, 2803442767, bitStream)
			self.CreateExtraPacketData(17, 1, 2803442767, bitStream)
			self.CreateExtraPacketData(5, 0, 2803442767, bitStream)
			self.CreateExtraPacketData(6, 1, 2803442767, bitStream)
			self.CreateExtraPacketData(20, 1, 2803442767, bitStream)
			self.CreateExtraPacketData(19, 30854, 2803442767, bitStream)
			self.CreateExtraPacketData(21, 0, 2803442767, bitStream)
			self.CreateExtraPacketData(22, 0, 2803442767, bitStream)
			self.CreateExtraPacketData(23, 4114, 2803442767, bitStream)
			self.CreateExtraPacketData(27, 4114, 2803442767, bitStream)
			self.CreateExtraPacketData(28, 1, 2803442767, bitStream)
			self.CreateExtraPacketData(29, 0, 2803442767, bitStream)
			self.CreateExtraPacketData(30, 30854, 2803442767, bitStream)
			################################End of the stamp stuff
			self.send(loginData, address, reliability=PacketReliability.ReliableOrdered)#Send packet
			#Register session
			if(loginResponse == LegoPackets.LOGIN_SUCCESS):
				info = getAccountByUsername(username)
				registerSession(str(address[0]), userkey, str(info[0]), str(0))


	def CreateExtraPacketData(self, stampID, bracketNum, afterNum, bitStream):
		bitStream[0].write(c_ulong(stampID))
		bitStream[0].write(c_long(bracketNum))
		bitStream[0].write(c_ulong(afterNum))
		bitStream[0].write(c_ulong(0))
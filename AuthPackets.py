import pyraknet.server as Server
from pyraknet.messages import Address
from pyraknet.bitstream import *
from Enum import *
from GameManager import Session, SessionState
from ServerUtilities import *
import uuid
from passlib.hash import sha256_crypt
from core import GameServer
from structures import CString

def HandleHandshake(Server : GameServer, data : bytes, address : Address):
	stream = ReadStream(data)
	clientVersion = stream.read(c_ulong)

	Server.send(getHandshake(clientVersion, 1), address)

def HandleLogin(Server : GameServer, data : bytes, address : Address):
	stream = ReadStream(data)

	#There's a lot of other stuff in this packet but I think this is all we really need
	username = stream.read(str, allocated_length=33)
	password = stream.read(str, allocated_length=41)

	packet, response, userKey = LoginResponse(Server, username, password)
	Server.send(packet, address)
	if(response == LoginResponseEnum.Success):
		session = Session(Server.Game)
		session.address = address
		session.userKey = userKey
		session.State = SessionState.LoggingIn
		session.accountUsername = username
		Server.Game.Sessions.append(session)

def LoginResponse(Server : Server, Username : str, Password: str):
	packet = WriteStream()
	userInfo = Server.Game.getAccountByUsername(Username)
	print("Attempted login with username '{}' and password '{}'".format(Username, Password))
	response = Server.checkLogin(Username, Password)
	writeHeader(packet, PacketHeader.LoginResponse)
	packet.write(c_uint8(response))
	packet.write(CString("Talk_Like_A_Pirate", allocated_length=33))
	packet.write(CString("", allocated_length=33*7))
	packet.write(c_ushort(1))
	packet.write(c_ushort(10))#Version Major, Current and Minor
	packet.write(c_ushort(64))
	userKey = (str(uuid.uuid4()))
	packet.write(userKey[0:18], allocated_length=33)
	packet.write(CString(Server.IP, allocated_length=33))#World Instance IP
	packet.write(CString(Server.IP, allocated_length=33))#Chat Instance IP
	packet.write(c_uint16(2002))#World Port
	packet.write(c_ushort(3003))#Chat Port
	packet.write(CString('0', allocated_length=33))#Some other IP
	packet.write(CString('00000000-0000-0000-0000-000000000000', allocated_length=37))
	packet.write(c_ulong(0))
	packet.write(CString('US', allocated_length=3))#US Localization
	packet.write(c_bool(False))
	packet.write(c_bool(False))
	packet.write(c_ulonglong(0))
	packet.write("Hello there ;D", length_type=c_uint16)#Custom error message
	packet.write(c_uint16(0))
	packet.write(c_ulong(4))
	return packet, response, userKey[0:18]
import pyraknet.server as Server
from pyraknet.messages import Address
from typing import Any, Callable
from passlib.hash import sha256_crypt
from enum import *
from GameManager import *
import AuthPackets
import threading
from ServerUtilities import *
from core import GameServer
from GameDB import GameDB

class AuthServer(GameServer):
	def __init__(self, address: Address, max_connections: int, incoming_password: bytes, GameManager : GameManager, CDClient : GameDB, ServerDB : GameDB):
		super().__init__(address, max_connections, incoming_password, GameManager, CDClient, ServerDB)
		self.add_handler(Server.Event.UserPacket, self.handlePacket)
		self.AuthHandlers = {}

		self.registerAuthHandler(PacketHeader.ClientLoginInfo.value, AuthPackets.HandleLogin)
		self.registerAuthHandler(PacketHeader.Handshake.value, AuthPackets.HandleHandshake)

		print("Auth Server Started")
	def handlePacket(self, data : bytes, address):
		if(data[0:8] in self.AuthHandlers):
			t = threading.Thread(target=self.AuthHandlers[data[0:8]], args=[self, data[8:], address])
			t.start()
		else:
			print("Header {} Has No Handler!".format(data[0:8]))
	def registerAuthHandler(self, header : PacketHeader, function : Callable):
		self.AuthHandlers[header] = function

	def checkLogin(self, Username : str, Password : str):
		userInfo = self.Game.getAccountByUsername(Username)
		response = None
		if (userInfo is not None and userInfo.Banned != True and sha256_crypt.verify(Password, userInfo.Password)):  # Success
			response = LoginResponseEnum.Success
			print("Login accepted!")
		else:  # Just put wrong info for now
			response = LoginResponseEnum.InvalidLoginInfo
		return response
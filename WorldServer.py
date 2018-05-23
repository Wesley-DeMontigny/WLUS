from typing import Callable
import WorldPackets
from PacketHeaders import PacketHeader
import threading
from ServerUtilities import *

class WorldServer(GameServer):
	def __init__(self, address: Address, max_connections: int, incoming_password: bytes, GameManager : GameManager):
		super().__init__(address, max_connections, incoming_password, GameManager)
		self.add_handler(Server.Event.UserPacket, self.handlePacket)
		self.WorldHandlers = {}

		self.registerWorldHandler(PacketHeader.ClientUserSessionInfo.value, WorldPackets.HandleSessionKey)
		self.registerWorldHandler(PacketHeader.ClientMinifigureListRequest.value, WorldPackets.HandleMinifigListRequest)
		self.registerWorldHandler(PacketHeader.Handshake.value, WorldPackets.HandleHandshake)
		print("World Server Started")
	def handlePacket(self, data : bytes, address):
		if(data[0:8] in self.WorldHandlers):
			t = threading.Thread(target=self.WorldHandlers[data[0:8]], args=[self, data[8:], address])
			t.start()
		else:
			print("Header {} Has No Handler!".format(data[0:8]))
	def registerWorldHandler(self, header : PacketHeader, function : Callable):
		self.WorldHandlers[header] = function

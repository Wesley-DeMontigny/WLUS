import pyraknet.server
import pyraknet.messages
import typing
import threading
import game_enums
import os
from pyraknet.bitstream import *


class WorldServer(pyraknet.server.Server):
	def __init__(self, address: pyraknet.messages.Address, max_connections: int, incoming_password: bytes, world_server_service):
		super().__init__(address, max_connections, incoming_password)
		self._world_server_service = world_server_service
		self.add_handler(pyraknet.server.Event.UserPacket, self.handle_packet)
		self._userpacket_handlers = {}

		self.register_userpacket_handler(game_enums.PacketHeaderEnum.HANDSHAKE.value, self.handle_handshake)

	def register_userpacket_handler(self, packet_header : bytes, handler : typing.Callable):
		self._userpacket_handlers[packet_header] = handler

	def handle_packet(self, data : bytes, address : pyraknet.messages.Address):
		if(data[0:8] in self._userpacket_handlers):
			t = threading.Thread(target=self._userpacket_handlers[data[0:8]], args=[data[8:], address])
			t.start()
		else:
			print("Header {} Has No Handler!".format(data[0:8]))

	def handle_handshake(self, data : bytes, address):
		stream = ReadStream(data)
		client_version = stream.read(c_ulong)

		packet = WriteStream()
		packet.write(game_enums.PacketHeaderEnum.HANDSHAKE.value)
		packet.write(c_ulong(client_version))
		packet.write(c_ulong(0x93))
		packet.write(c_ulong(4))  # Connection Type (1 For Auth, 4 For Everything Else)
		packet.write(c_ulong(os.getpid()))
		packet.write(c_short(0xff))  # Local port
		packet.write(self._world_server_service.get_parent().get_config("address"), allocated_length=33)

		self.send(packet, address)
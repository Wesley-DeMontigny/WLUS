import services
import pyraknet.server
import pyraknet.messages
from pyraknet.bitstream import *
import game_enums
import copy
import game_types


class ChatServerService(services.GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Chat Server"
		self.blacklist = []

		if (parent.get_config("chat_port") is not None):
			self._port = parent.get_config("chat_port")
		else:
			self._port = 3003

		if (parent.get_config("bind_address") is not None):
			self._address = parent.get_config("bind_address")
		else:
			self._address = "127.0.0.1"

		if (parent.get_config("world_max_connections") is not None):#Since you would only be connected to the Chat Server if you were also connected to the World Server why not make them the same
			self._max_connections = parent.get_config("world_max_connections")
		else:
			self._max_connections = 10

		self.server = ChatServer((self._address, self._port), max_connections=self._max_connections, incoming_password=b"3.25 ND1", chat_server_service=self)

		global game
		game = self.get_parent()

	def initialize(self):
		for handler in self.server.default_handlers:
			self.get_parent().register_event_handler(self.server.default_handlers[handler][0])(self.server.default_handlers[handler][1])
		super().initialize()


class ChatServer(pyraknet.server.Server):
	def __init__(self, address: pyraknet.messages.Address, max_connections: int, incoming_password: bytes, chat_server_service):
		super().__init__(address, max_connections, incoming_password)
		self.chat_server_service = chat_server_service
		self.add_handler(pyraknet.server.Event.UserPacket, self.handle_packet)
		self.default_handlers = {"chat_whitelist_request":["OnPacket_World_{}".format(game_enums.PacketHeaderEnum.CLIENT_WHITELIST_REQUEST.value), self.handle_whitelist_request]}
		global game
		game = self.chat_server_service.get_parent()


	def handle_whitelist_request(self, data : bytes, address):#Just make the whole "accepted" and filter out any bad words when we send the actual message
		request_packet = ReadStream(data)
		super_chat_level = request_packet.read(c_uint8)
		request_id = request_packet.read(c_uint8)

		stream = WriteStream()
		stream.write(game_enums.PacketHeaderEnum.CHAT_MODERATION_RESPONSE.value)
		stream.write(c_bit(True))
		stream.write(c_uint16(0))
		stream.write(c_uint8(request_id))
		stream.write(c_uint8(0))
		stream.write(game_types.String("", allocated_length=66))
		length = int(len(copy.deepcopy(stream).__bytes__()))
		stream.write(game_types.String("", allocated_length=99-length))
		stream.write(c_uint8(0))
		stream.write(c_uint8(0))

		ws = game.get_service("World Server")
		ws.server.send(stream, address)#Doesn't work for some reason, i'll have to check it out



	def handle_packet(self, data : bytes, address : pyraknet.messages.Address):
		game.trigger_event("OnPacket_Chat_{}".format(str(data[0:8])), args=[data[8:], address], debug=True)

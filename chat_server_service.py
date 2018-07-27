import services
import pyraknet.server
import pyraknet.messages


class ChatServerService(services.GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Chat Server"

		if (parent.get_config("chat_port") is not None):
			self._port = parent.get_config("chat_port")
		else:
			self._port = 3003

		if (parent.get_config("bind_address") is not None):
			self._address = parent.get_config("bind_address")
		else:
			self._address = "127.0.0.1"

		if (parent.get_config("chat_max_connections") is not None):
			self._max_connections = parent.get_config("chat_max_connections")
		else:
			self._max_connections = 10

		self.server = ChatServer((self._address, self._port), max_connections=self._max_connections, incoming_password=b"3.25 ND1", chat_server_service=self)

	def initialize(self):
		for handler in self.server.default_handlers:
			self.get_parent().register_event_handler(self.server.default_handlers[handler][0])(self.server.default_handlers[handler][1])
		super().initialize()


class ChatServer(pyraknet.server.Server):
	def __init__(self, address: pyraknet.messages.Address, max_connections: int, incoming_password: bytes, chat_server_service):
		super().__init__(address, max_connections, incoming_password)
		self.chat_server_service = chat_server_service
		self.add_handler(pyraknet.server.Event.UserPacket, self.handle_packet)
		self.default_handlers = {}
		global game
		game = self.chat_server_service.get_parent()


	def handle_packet(self, data : bytes, address : pyraknet.messages.Address):
		game.trigger_event("OnPacket_Chat_{}".format(str(data[0:8])), args=[data[8:], address], debug=True)

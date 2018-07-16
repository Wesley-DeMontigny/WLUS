import services
from pyraknet.bitstream import *
import copy
import game_enums


class ChatCommandService(services.GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Chat Command"
		self._commands = {}
		global game
		game = self.get_parent()

	def initialize(self):
		self.register_command("/testmap", self.testmap)
		game.register_event_handler("GM_{}".format(game_enums.GameMessages.PARSE_CHAT_MSG.value))(self.handle_command)
		super().initialize()

	def handle_command(self, object_id, stream, address):
		client_state = stream.read(c_int)
		command = stream.read(str, length_type=c_ulong)
		args = command.split(" ")
		if(game.get_config("allow_commands") == True or bool(game.get_service("Player").get_account_by_player_id(object_id)["is_admin"]) == True):
			if(args[0] in self._commands):
				copy_args = copy.deepcopy(args)
				del copy_args[0]
				self._commands[args[0]](object_id, address, copy_args, client_state)

	def register_command(self, command_name, handler):
		self._commands[command_name] = handler

	def testmap(self, object_id, address, args, client_state):
		if(game.get_service("World").get_zone_by_id(int(args[0])) is not None):
			world_server = game.get_service("World Server").server
			world_server.load_world(object_id, int(args[0]), address, True)







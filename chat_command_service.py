import services
from pyraknet.bitstream import *
import copy
import game_enums
import components


class ChatCommandService(services.GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Chat Command"
		self._commands = {}
		global game
		game = self.get_parent()

	def initialize(self):
		self.register_command("/testmap", self.testmap)
		self.register_command("/togglejetpack", self.toggle_jetpack)
		self.register_command("/additem", self.get_item)
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

	def get_item(self, object_id, address, args, client_state):
		try:
			lot = int(args[0])
			player_service = game.get_service("Player")
			item = player_service.add_item_to_inventory(object_id, lot, json_data={"from_command":1})
			if(item is not None):
				game.get_service("Game Message").add_item_to_inventory_client_sync(object_id, [address], item["lot"], item["item_id"], item["slot"])
		except Exception as e:
			print("Error While Getting Item", e)

	def toggle_jetpack(self, object_id, address, args, client_state):
		player = game.get_service("Player").get_player_object_by_id(object_id)
		zone = player.zone
		if(player is not None):
			game.get_service("Game Message").set_jetpack_mode(object_id, zone.get_connections(), bypass_checks=True, use=not player.get_component(components.Character).jetpack_enabled, air_speed=20,
															  max_air_speed=30, vert_vel=2, effect_id=36)
			player.get_component(components.Character).jetpack_enabled = not player.get_component(components.Character).jetpack_enabled

	def testmap(self, object_id, address, args, client_state):
		if(game.get_service("World").get_zone_by_id(int(args[0])) is not None):
			world_server = game.get_service("World Server").server
			world_server.load_world(object_id, int(args[0]), address, True)







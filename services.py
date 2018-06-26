import game_types
import typing
import auth_server
import passlib.hash
import database
import world_server
import scene

'''
Services are a way to implement new parts of the server architecture.
They can each access each other through self.get_parent().get_service("SERVICE NAME").
A service's parent should always be Game, although I'm not sure you could do it any other way even if you tried.
'''


class GameService(game_types.BaseObject):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Base Service"

	def initialize(self):
		self.get_parent().trigger_event("ServiceInitialized", args=(self,), debug=False)
		print("Initializied {} Service".format(self._name))


class WorldService(GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "World"
		self._scenes : typing.List[scene.Scene] = []

	def add_scene(self, level : int, name : str = "Scene"):
		self._scenes.append(scene.Scene(self, level, name))

	def get_scene_by_id(self, id : int):
		for scene in self._scenes:
			if(scene.get_id() == id):
				return scene
		return None

	def get_scenes_by_level(self, level : int):
		scenes = []
		for scene in self._scenes:
			if(scene.get_levelid() == level):
				scenes.append(scene)
		return scenes

class AuthServerService(GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Auth Server"

		if(parent.get_config("auth_port") is not None):
			self._port = parent.get_config("auth_port")
		else:
			self._port = 1001

		if(parent.get_config("address") is not None):
			self._address = parent.get_config("address")
		else:
			self._address = "127.0.0.1"

		if(parent.get_config("auth_max_connections") is not None):
			self._max_connections = parent.get_config("auth_max_connections")
		else:
			self._max_connections = 10

		self.server = auth_server.AuthServer((self._address, self._port), max_connections=self._max_connections, incoming_password=b"3.25 ND1", auth_server_service=self)

	def initialize(self):
		super().initialize()
		for handler in self.server.default_handlers:
				self.get_parent().register_event_handler(self.server.default_handlers[handler][0])(self.server.default_handlers[handler][1])

	def validate_login(self, username : str, password : str):
		server_db : database.GameDB = self._parent.get_service("Database").server_db
		account_table : database.DBTable = server_db.tables["Accounts"]
		user_info = account_table.select_all("username = '{}'".format(username))[0]
		if (user_info is not None and bool(user_info["banned"]) != True and passlib.hash.sha256_crypt.verify(password, user_info["password"])):  # Success
			return True, user_info
		else:
			return False, user_info

class DatabaseService(GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Database"

		self.cdclient_db = database.GameDB("resources/cdclient.sqlite")
		self.server_db = database.GameDB("server.sqlite")


class WorldServerService(GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "World Server"

		if(parent.get_config("world_port") is not None):
			self._port = parent.get_config("world_port")
		else:
			self._port = 2002

		if(parent.get_config("address") is not None):
			self._address = parent.get_config("address")
		else:
			self._address = "127.0.0.1"


		if(parent.get_config("world_max_connections") is not None):
			self._max_connections = parent.get_config("world_max_connections")
		else:
			self._max_connections = 10

		self.server = world_server.WorldServer((self._address, self._port), max_connections=self._max_connections, incoming_password=b"3.25 ND1", world_server_service=self)

	def initialize(self):
		super().initialize()
		for handler in self.server.default_handlers:
			self.get_parent().register_event_handler(self.server.default_handlers[handler][0])(self.server.default_handlers[handler][1])

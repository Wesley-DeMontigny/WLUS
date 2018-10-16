import game_types
import typing
import auth_server
import bcrypt
import database
import world_server
import zone
import sys

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

	def get_name(self):
		return self._name

class WorldService(GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "World"
		self._zones : typing.List[zone.Zone] = []

	def register_zone(self, zone_id : int, load_id : int, checksum : int, activity : bool = False, spawn_loc : game_types.Vector3 = game_types.Vector3(0,0,0), spawn_rot : game_types.Vector4 = game_types.Vector4(), name : str = "Zone", json : dict = None):
		if(self.get_zone_by_id(zone_id) is None):
			new_zone = zone.Zone(self, zone_id, load_id, checksum, name, activity, spawn_loc, spawn_rot, json)
			self._zones.append(new_zone)
			self.get_parent().trigger_event("ZoneRegistered", args=(new_zone,))
		else:
			raise Exception("A ZONE WITH THE ID {} WAS ALREADY REGISTERED!".format(zone_id))

	def get_zone_by_id(self, id : int):
		for zone in self._zones:
			if(zone.get_zone_id() == id):
				return zone
		return None

	def get_zones(self):
		return self._zones

class AuthServerService(GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Auth Server"

		if(parent.get_config("auth_port") is not None):
			self._port = parent.get_config("auth_port")
		else:
			self._port = 1001

		if(parent.get_config("bind_address") is not None):
			self._address = parent.get_config("bind_address")
		else:
			self._address = "127.0.0.1"

		if(parent.get_config("auth_max_connections") is not None):
			self._max_connections = parent.get_config("auth_max_connections")
		else:
			self._max_connections = 10

		self.server = auth_server.AuthServer((self._address, self._port), max_connections=self._max_connections, incoming_password=b"3.25 ND1", auth_server_service=self)

	def initialize(self):
		for handler in self.server.default_handlers:
				self.get_parent().register_event_handler(self.server.default_handlers[handler][0])(self.server.default_handlers[handler][1])
		super().initialize()

	def validate_login(self, username : str, password : str):
		server_db : database.GameDB = self._parent.get_service("Database").server_db
		c = server_db.connection.cursor()
		c.execute("SELECT * FROM Accounts WHERE username = ?", (username,))
		user_info = c.fetchone()
		if (user_info is not None and bool(user_info["banned"]) != True and bcrypt.checkpw(password.encode("utf-8"), user_info["password"].encode("utf-8"))):  # Success
			return True, user_info
		else:
			return False, user_info

	def register_account(self, username : str, password : str, banned = 0, is_admin = 0):
		passhash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
		server_db : database.GameDB = self._parent.get_service("Database").server_db
		c = server_db.connection.cursor()
		c.execute("INSERT INTO Accounts (username, password, banned, is_admin) VALUES (?, ?, ?, ?)", (username, passhash, banned, is_admin))
		print(f"Registered User '{username}'")

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

		if(parent.get_config("bind_address") is not None):
			self._address = parent.get_config("bind_address")
		else:
			self._address = "127.0.0.1"


		if(parent.get_config("world_max_connections") is not None):
			self._max_connections = parent.get_config("world_max_connections")
		else:
			self._max_connections = 10

		self.server = world_server.WorldServer((self._address, self._port), max_connections=self._max_connections, incoming_password=b"3.25 ND1", world_server_service=self)

	def initialize(self):
		for handler in self.server.default_handlers:
			self.get_parent().register_event_handler(self.server.default_handlers[handler][0])(self.server.default_handlers[handler][1])
		super().initialize()

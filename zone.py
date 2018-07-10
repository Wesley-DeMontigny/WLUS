import game_types
import game_objects
import game_enums
from pyraknet.bitstream import *
from pyraknet.messages import *
import pyraknet.replicamanager
import typing

'''
All Game Objects are children to a scene.
'''


class Zone(game_types.BaseObject):
	def __init__(self, parent, zone_id: int, load_id: int, checksum: int, name: str = "Zone", activity: bool = False, spawn_loc : game_types.Vector3 = game_types.Vector3(0,0,0), pvp_enabled : bool = False):
		super().__init__(parent)
		self._zone_id = zone_id
		self._load_id = load_id
		self._checksum = checksum
		self.spawn_loc = spawn_loc
		self.pvp_enabled = pvp_enabled
		self._name = name
		self._objects = []
		self._replica_manager: ZoneManager = ZoneManager(self.get_parent().get_parent().get_service("World Server").server)
		self._players = []
		self._activity = activity

	def get_zone_id(self):
		return self._zone_id

	def get_load_info(self):
		return self._load_id, self._checksum, self._activity, self.spawn_loc, self._name

	def update(self, game_object):
		if(isinstance(game_object, game_objects.ReplicaObject)):
			self._replica_manager.serialize(game_object)

	def get_object_by_id(self, object_id):
		for object in self._objects:
			if(object.get_object_id() == object_id):
				return object
		return None

	def create_object(self, parent, config : dict):
		game_object = game_objects.ReplicaObject(parent, self, config)
		self._objects.append(game_object)

	def destroy_object(self, object):
		self._replica_manager.destruct(object)
		self._objects.remove(object)

	def add_player(self, player_id: int):
		self._players.append(player_id)
		sessions = self.get_parent().get_parent().get_service("Session")
		player_session = sessions.get_session_by_player_id(player_id)
		self._replica_manager.add_participant(player_session.address)
		player_session.scene_id = self.get_py_id()

	def remove_player(self, player_id: int):
		self._players.remove(player_id)
		sessions = self.get_parent().get_parent().get_service("Session")
		player_session = sessions.get_session_by_player_id(player_id)
		self._replica_manager.remove_participant(player_session.address)
		player_session.scene_id = 0
		self.destroy_object(self.get_object_by_id(player_id))


class ZoneManager(pyraknet.replicamanager.ReplicaManager):
	def __init__(self, server):
		super().__init__(server)
		global game
		game = server.world_server_service.get_parent()
		global replica_service
		replica_service = game.get_service('Replica')

	def remove_participant(self, address):
		self._participants.discard(address)

	def serialize(self, obj: game_objects.ReplicaObject) -> None:
		out = WriteStream()
		out.write(c_ubyte(Message.ReplicaManagerSerialize))
		out.write(c_ushort(self._network_ids[obj]))
		replica_service.write_to_stream(obj, out, game_enums.ReplicaTypes.SERIALIZATION)

		self._server.send(out, self._participants)

	def construct(self, obj: game_objects.ReplicaObject, new: bool = True, recipients: typing.Iterable[Address] = None):
		self._construct(obj, new, recipients)

	def _construct(self, obj: game_objects.ReplicaObject, new: bool=True, recipients: typing.Iterable[Address]=None) -> None:
		# recipients is needed to send replicas to new participants
		if recipients is None:
			recipients = self._participants

		if new:
			self._network_ids[obj] = self._current_network_id
			self._current_network_id += 1

		out = WriteStream()
		out.write(c_ubyte(Message.ReplicaManagerConstruction))
		out.write(c_bit(True))
		out.write(c_ushort(self._network_ids[obj]))
		replica_service.write_to_stream(obj, out, game_enums.ReplicaTypes.CONSTRUCTION)

		self._server.send(out, recipients)
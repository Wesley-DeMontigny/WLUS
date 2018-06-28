import game_types
import game_objects
from pyraknet.bitstream import *
from pyraknet.messages import *
import pyraknet.replicamanager
import typing

'''
Scenes are essentially instances of any particular zone. All Game Objects are children to a scene.
'''


class Scene(game_types.BaseObject):
	def __init__(self, parent, levelid: int = 0, name: str = "Scene", activity: bool = False):
		super().__init__(parent)
		self._levelid: int = levelid
		self._name = name
		self._objects = []
		self._replica_manager: SceneManager = SceneManager(self.get_parent().get_parent().get_service("World Server").server)
		self._players = []
		self._activity = activity

	def is_activity(self):
		return self._activity

	def get_levelid(self):
		return self._levelid

	def update(self, game_object):
		if(isinstance(game_object, game_objects.ReplicaObject)):
			self._replica_manager.serialize(game_object)

	def get_object_by_id(self, object_id):
		for object in self._objects:
			if(object.get_object_id() == object_id):
				return object
		return None

	def create_object(self, object):
		self._objects.append(object)

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


class SceneManager(pyraknet.replicamanager.ReplicaManager):
	def __init__(self, server):
		super().__init__(server)

	def remove_participant(self, address):
		self._participants.discard(address)

	def serialize(self, obj: typing.Any) -> None:
		out = WriteStream()
		out.write(c_ubyte(Message.ReplicaManagerSerialize))
		out.write(c_ushort(self._network_ids[obj]))
		obj.serialize(out)

		self._server.send(out, self._participants)

	def construct(self, obj: typing.Any, new: bool = True, recipients: typing.Iterable[Address] = None):
		self._construct(obj, new, recipients)
import game_types
import game_objects
from pyraknet.bitstream import *
from pyraknet.messages import *
import pyraknet.replicamanager
import typing

class Scene(game_types.BaseObject):
	def __init__(self, parent, levelid: int = 0, name: str = "Scene"):
		super().__init__(parent)
		self._levelid: int = levelid
		self._name = name
		self._replica_manager: SceneManager = SceneManager(
			self.get_parent().get_parent().get_service("World Server").server)
		self._players = []

	def get_levelid(self):
		return self._levelid

	def update(self, game_object):
		if(isinstance(game_object, game_objects.ReplicaObject)):
			self._replica_manager.serialize(game_object)

	def add_player(self, player_id: int):
		self._players.append(player_id)
		sessions = self.get_parent().get_parent().get_service("Session")
		player_session = sessions.get_session_by_player_id(player_id)
		self._replica_manager.add_participant(player_session.address)
		player_session.scene_id = self.get_id()

	def remove_player(self, player_id: int):
		self._players.remove(player_id)
		sessions = self.get_parent().get_parent().get_service("Session")
		player_session = sessions.get_session_by_player_id(player_id)
		self._replica_manager.remove_participant(player_session.address)
		player_session.scene_id = 0


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
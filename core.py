import pyraknet
import GameManager
import GameDB
from pyraknet.bitstream import *
from pyraknet.replicamanager import ReplicaManager
from pyraknet.messages import Address, Message
from typing import Any, Iterable

class GameServer(pyraknet.server.Server):
	def __init__(self, address: pyraknet.messages.Address, max_connections: int, incoming_password: bytes, GameManager : GameManager.GameManager, CDClient : GameDB.GameDB):
		super().__init__(address, max_connections, incoming_password)
		self.Game : GameManager = GameManager
		self.CDClient : GameDB.GameDB = CDClient

class GameReplicaManager(ReplicaManager):
	def __init__(self, Server : GameServer):
		super().__init__(Server)
	def remove_participant(self, address : Address):
		self._participants.discard(address)
	def construct(self, obj: Any, new: bool=True, recipients: Iterable[Address]=None):
		self._construct(obj, new, recipients)
	def serialize(self, obj: Any) -> None:

		out = WriteStream()
		out.write(c_ubyte(Message.ReplicaManagerSerialize))
		out.write(c_ushort(self._network_ids[obj]))
		obj.serialize(out)

		self._server.send(out, self._participants)
	def destruct(self, obj: Any) -> None:

		obj.on_destruction()
		out = WriteStream()
		out.write(c_ubyte(Message.ReplicaManagerDestruction))
		out.write(c_ushort(self._network_ids[obj]))

		for participant in self._participants:
			self._server.send(out, participant)

		del self._network_ids[obj]
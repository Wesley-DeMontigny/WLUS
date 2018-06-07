import pyraknet
import GameDB
from pyraknet.bitstream import *
from pyraknet.replicamanager import ReplicaManager
from pyraknet.messages import Address, Message
from typing import Any, Iterable
from ServerUtilities import writeHeader
from PacketHeaders import PacketHeader
from Enum import ZoneID

class GameServer(pyraknet.server.Server):
	def __init__(self, address: pyraknet.messages.Address, max_connections: int, incoming_password: bytes, GameManager, CDClient : GameDB, ServerDB : GameDB):
		super().__init__(address, max_connections, incoming_password)
		self.Game = GameManager
		self.IP = address[0]
		self.ServerDB = ServerDB
		self.CDClient : GameDB.GameDB = CDClient

	def brodcastPacket(self, data : WriteStream, ZoneID : ZoneID):
		connections = self.Game.getConnectionsInZone(ZoneID)
		for connection in connections:
			self.send(data, connection)

	def InitializeGameMessage(self, stream: WriteStream, objectID: int, messageID: int):
		writeHeader(stream, PacketHeader.ServerGameMessage)
		stream.write(c_longlong(objectID))
		stream.write(c_uint16(messageID))

class GameReplicaManager(ReplicaManager):
	def __init__(self, Server : GameServer):
		super().__init__(Server)

	def remove_participant(self, address : Address):
		self._participants.discard(address)

	def get_participants(self):
		return self._participants

	def construct(self, obj: Any, new: bool=True, recipients: Iterable[Address]=None):
		self._construct(obj, new, recipients)

	def _construct(self, obj: Any, new: bool=True, recipients: Iterable[Address]=None) -> None:
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
		obj.write_construction(out)
		outBytes = bytes(out)

		self._server.send(outBytes, recipients)

	def serialize(self, obj: Any, recipients : Iterable[Address]=None) -> None:

		if recipients is None:
			recipients = self._participants

		out = WriteStream()
		out.write(c_ubyte(Message.ReplicaManagerSerialize))
		out.write(c_ushort(self._network_ids[obj]))
		obj.serialize(out)

		self._server.send(out, recipients)

	def destruct(self, obj: Any) -> None:

		obj.on_destruction()
		out = WriteStream()
		out.write(c_ubyte(Message.ReplicaManagerDestruction))
		out.write(c_ushort(self._network_ids[obj]))

		for participant in self._participants:
			self._server.send(out, participant)

		del self._network_ids[obj]

	def is_participant(self, address : Address):
		return (address in self._participants)
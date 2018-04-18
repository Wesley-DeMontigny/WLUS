################
#Created by lcdr
################
import asyncio

from bitstream import BitStream, c_bit, c_ubyte, c_ushort
from messages import Message

class ReplicaManager:
	def __init__(self, server):
		self._participants = set()
		self._network_ids = {}
		self._current_network_id = 0
		self.server = server
		asyncio.ensure_future(self._serialize_loop())

	def add_participant(self, address):
		self._participants.add(address)
		for obj in self._network_ids:
			self.construct(obj, (address,), new=False)

	def on_disconnect_or_connection_lost(self, data, address):
		self._participants.discard(address)

	def construct(self, obj, recipients=None, new=True, constructMsg=None, logFile=None):
		# recipients is needed to send replicas to new participants
		if recipients is None:
			recipients = self._participants

		if new:
			self._network_ids[obj] = self._current_network_id
			self._current_network_id += 1

		out = BitStream()
		out.write(c_ubyte(Message.ReplicaManagerConstruction))
		out.write(c_bit(True))
		out.write(c_ushort(self._network_ids[obj]))
		out.write(obj.send_construction())

		if(logFile != None):
			log = open(logFile, "wb")
			log.write(out)
		if (constructMsg != None):
			print("[" + self.server.role + "]" + constructMsg)
		else:
			print("[" + self.server.role + "]" + "Used replica constructor")

		for recipient in recipients:
			self.server.send(out, recipient)

	def serialize(self, obj):
		out = BitStream()
		out.write(c_ubyte(Message.ReplicaManagerSerialize))
		out.write(c_ushort(self._network_ids[obj]))
		out.write(obj.serialize())
		for participant in self._participants:
			self.server.send(out, participant)

	def destruct(self, obj):
		print("destructing", obj)
		obj.on_destruction()
		out = BitStream()
		out.write(c_ubyte(Message.ReplicaManagerDestruction))
		out.write(c_ushort(self._network_ids[obj]))

		for participant in self._participants:
			self.server.send(out, participant)

		del self._network_ids[obj]

	@asyncio.coroutine
	def _serialize_loop(self):
		while True:
			for obj in self._network_ids:
				if obj._serialize:
					self.serialize(obj)
					obj._serialize = False
			yield from asyncio.sleep(0.03)
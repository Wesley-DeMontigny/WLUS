import pyraknet
import GameManager
import GameDB
from pyraknet.bitstream import *

class GameServer(pyraknet.server.Server):
	def __init__(self, address: pyraknet.messages.Address, max_connections: int, incoming_password: bytes, GameManager : GameManager.GameManager, CDClient : GameDB.GameDB):
		super().__init__(address, max_connections, incoming_password)
		self.Game : GameManager = GameManager
		self.CDClient : GameDB.GameDB = CDClient

#Ripped this straight off of PYLUS Because I had no idea how to make the char_size of strings equal to 1. Idk why it was removed as a parameter but whatever I guess
class CString(Serializable):
	def __init__(self, data='', allocated_length=None, length_type=None):
		self.data = data
		self.allocated_length = allocated_length
		self.length_type = length_type

	def serialize(self, stream):
		stream.write(self.data if isinstance(self.data, bytes) else bytes(self.data, 'latin1'),
					 allocated_length=self.allocated_length, length_type=self.length_type)

	def deserialize(self, stream):
		return stream.read(bytes, allocated_length=self.allocated_length, length_type=self.length_type).decode('latin1')
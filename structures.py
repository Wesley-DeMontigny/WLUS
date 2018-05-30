from pyraknet.bitstream import *

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


class Vector3():
	def __init__(self, X : float, Y : float, Z : float):
		self.X : float = X
		self.Y : float = Y
		self.Z : float = Z
	def translate(self, X : float, Y : float, Z : float):
		self.X += X
		self.Y += Y
		self.Z += Z
	def set(self, X : float, Y : float, Z : float):
		self.X = X
		self.Y = Y
		self.Z = Z

class Vector4():
	def __init__(self, X : float, Y : float, Z : float, W : float):
		self.X : float = X
		self.Y : float = Y
		self.Z : float = Z
		self.W : float = W
	def translate(self, X : float, Y : float, Z : float, W : float):
		self.X += X
		self.Y += Y
		self.Z += Z
		self.W += W
	def set(self, X : float, Y : float, Z : float, W : float):
		self.X = X
		self.Y = Y
		self.Z = Z
		self.W = W

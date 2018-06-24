import threading
import typing
from pyraknet.bitstream import *
import pyraknet.replicamanager
from pyraknet.messages import *

class BaseObject():
	def __init__(self, parent):
		self._name = "Name"
		self._parent = parent
		self._children = []
		self._id = id(self)
		self._scripts = {}
		if(isinstance(self._parent, BaseObject)):
			self._parent._children.append(self)

	def get_name(self):
		return self._name

	def get_id(self):
		return self._id

	def set_name(self, name : str):
		self._name = name

	def add_script(self, script):
		script_thread = GameThread(target=script.run)
		script_thread.start()
		self._scripts[script.get_name()] = script_thread

	def remove_script(self, script_name : str):
		thread_list = threading.enumerate()
		for thread in thread_list:
			if(thread == self._scripts[script_name]):
				thread.stop()
				del self._scripts[script_name]
				return

	def get_parent(self):
		return self._parent

	def get_children(self):
		return self._children


class GameThread(threading.Thread):
	def stop(self):
		self._stop()

class String(Serializable):
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
	def __init__(self, X : float = 0.0, Y : float = 0.0, Z : float = 0.0):
		self.X : float = X
		self.Y : float = Y
		self.Z : float = Z

	def __add__(self, other):
		return Vector3(self.X + other.X,self.Y + other.Y,self.Z + other.Z)

	def __sub__(self, other):
		return Vector3(self.X - other.X, self.Y - other.Y, self.Z - other.Z)

	def set(self, X : float, Y : float, Z : float):
		self.X = X
		self.Y = Y
		self.Z = Z

class Vector4():
	def __init__(self, X : float = 0.0, Y : float = 0.0, Z : float = 0.0, W : float = 0.0):
		self.X : float = X
		self.Y : float = Y
		self.Z : float = Z
		self.W : float = W

	def __add__(self, other):
		return Vector4(self.X + other.X, self.Y + other.Y, self.Z + other.Z, self.W + other.W)

	def __sub__(self, other):
		return Vector4(self.X - other.X, self.Y - other.Y, self.Z - other.Z, self.W - other.W)

	def set(self, X : float, Y : float, Z : float, W : float):
		self.X = X
		self.Y = Y
		self.Z = Z
		self.W = W



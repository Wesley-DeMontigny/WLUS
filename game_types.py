import threading
import typing
from pyraknet.bitstream import *
import pyraknet.replicamanager
from pyraknet.messages import *
from xml.etree import ElementTree

class BaseObject():
	def __init__(self, parent):
		self._name = "Name"
		self._parent = parent
		self._children = []
		self._scripts = {}
		if(isinstance(self._parent, BaseObject)):
			self._parent._children.append(self)

	def get_name(self):
		return self._name

	def get_py_id(self):
		return id(self)

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
		self._tstate_lock = None
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
	def __init__(self, X : float = 0.0, Y : float = 0.0, Z : float = 0.0, str_val:str = None):
		self.X : float = X
		self.Y : float = Y
		self.Z : float = Z
		if(str_val is not None):
			vector_list = str_val.split(",")
			self.X = float(vector_list[0])
			self.Y = float(vector_list[1])
			self.Z = float(vector_list[2])

	def __add__(self, other):
		return Vector3(self.X + other.X,self.Y + other.Y,self.Z + other.Z)

	def __sub__(self, other):
		return Vector3(self.X - other.X, self.Y - other.Y, self.Z - other.Z)

	def set(self, X : float, Y : float, Z : float):
		self.X = X
		self.Y = Y
		self.Z = Z

	def __str__(self):
		return "{},{},{}".format(self.X, self.Y, self.Z)

	def __eq__(self, other):
		if(self.X == other.X and self.Y == other.Y and self.Z == other.Z):
			return True
		else:
			return False

class LDF(Serializable):
	def __init__(self):
		self._keys : list = []
	def register_key(self, key_name : str, value : any, type : int):
		self._keys.append([key_name, value, type])
	def serialize(self, stream):
		key_num = len(self._keys)
		stream.write(c_uint(key_num))
		for key in self._keys:
			name = key[0]
			value = key[1]
			type = key[2]
			stream.write(c_uint8(len(name) * 2))
			for char in name:
				stream.write(char.encode('latin1'))
				stream.write(b'\0')
			stream.write(c_ubyte(type))
			if(type == 0):
				stream.write(value, length_type=c_uint)
			elif(type == 1):
				stream.write(c_int(value))
			elif(type == 3):
				stream.write(c_float(value))
			elif(type == 5):
				stream.write(c_uint(value))
			elif(type == 7):
				stream.write(c_bool(value))
			elif(type == 8 or type == 9):
				stream.write(c_int64(value))
			elif(type == 13):
				xml_str = bytes(ElementTree.tostring(value))
				xml_str = b'<?xml version="1.0">' + xml_str
				stream.write(c_ulong(xml_str.__len__()))
				stream.write(xml_str)
	def deserialize(self, stream):
		return "Not Implemented"

class Vector4():
	def __init__(self, X : float = 0.0, Y : float = 0.0, Z : float = 0.0, W : float = 0.0, str_val: str = None):
		self.X : float = X
		self.Y : float = Y
		self.Z : float = Z
		self.W : float = W
		if(str_val is not None):
			vector_list = str_val.split(",")
			self.X = float(vector_list[0])
			self.Y = float(vector_list[1])
			self.Z = float(vector_list[2])
			self.W = float(vector_list[3])

	def __add__(self, other):
		return Vector4(self.X + other.X, self.Y + other.Y, self.Z + other.Z, self.W + other.W)

	def __sub__(self, other):
		return Vector4(self.X - other.X, self.Y - other.Y, self.Z - other.Z, self.W - other.W)

	def set(self, X : float, Y : float, Z : float, W : float):
		self.X = X
		self.Y = Y
		self.Z = Z
		self.W = W

	def __str__(self):
		return "{},{},{},{}".format(self.X, self.Y, self.Z, self.W)



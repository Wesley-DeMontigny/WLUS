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


class Vector3(Serializable):
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

	def serialize(self, stream):
		stream.write(c_float(self.X))
		stream.write(c_float(self.Y))
		stream.write(c_float(self.Z))

	def deserialize(self, stream):
		return Vector3(stream.read(c_float), stream.read(c_float), stream.read(c_float))

class LDF(Serializable):
	def __init__(self):
		self._keys : list = []
	def register_key(self, key_name : str, value : any, type : int):
		self._keys.append([key_name, value, type])
	def __str__(self):
		return str(self._keys)
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

class Vector4(Serializable):
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

	def __eq__(self, other):
		if(self.X == other.X and self.Y == other.Y and self.Z == other.Z, self.W == other.W):
			return True
		else:
			return False

	def serialize(self, stream):
		stream.write(c_float(self.X))
		stream.write(c_float(self.Y))
		stream.write(c_float(self.Z))
		stream.write(c_float(self.W))

	def deserialize(self, stream):
		return Vector4(stream.read(c_float), stream.read(c_float), stream.read(c_float), stream.read(c_float))


class LVL(Serializable):
	def __init__(self, config : dict = None):
		self.config = config


	def serialize(self, stream):
		raise NotImplementedError

	#TODO: This is a super lazy version of what it should actually be doing, definitely need to fix this up
	def deserialize(self, stream):
		config = {}
		config["objects"] = []
		while True:
			try:
				buffer = b""
				for i in range(4):
					character = stream.read(bytes, length=1)
					buffer = buffer + character
				if (buffer == b"CHNK"):
					chunk_type = stream.read(c_ulong)
					stream.read(c_uint16)
					stream.read(c_uint16)
					stream.read(c_ulong)
					stream.read(bytes, length=int((stream.read(c_ulong) * 8 - int(stream.read_offset)) / 8))
					if (chunk_type == 1000):
						config["version"] = stream.read(c_ulong)
						stream.read(c_ulong)
						stream.read(c_ulong)
						stream.read(c_ulong)
						stream.read(c_ulong)
					elif (chunk_type == 2001):
						for i in range(stream.read(c_ulong)):
							gameobject = {}
							gameobject["object_id"] = stream.read(c_ulonglong)
							gameobject["lot"] = stream.read(c_ulong)
							if (config["version"] >= 0x26):
								stream.read(c_ulong)
							if (config["version"] >= 0x20):
								stream.read(c_ulong)
							gameobject["position"] = Vector3().deserialize(stream)
							w_rot = stream.read(c_float)
							x_rot = stream.read(c_float)
							y_rot = stream.read(c_float)
							z_rot = stream.read(c_float)
							gameobject["rotation"] = Vector4(x_rot, y_rot, z_rot, w_rot)
							gameobject["scale"] = stream.read(c_float)
							gameobject["ldf"] = self._read_ldf(stream.read(str, length_type=c_ulong))
							if (config["version"] >= 7):
								stream.read(c_ulong)
							config["objects"].append(gameobject)
						break
			except Exception as e:
				#print("Error while parsing LVL", e)
				#Because of this sloppy implementation theres always a dumb error or two
				break
		return LVL(config)

	def _read_ldf(self, ldf):
		ldf_dict = {}
		key_sets = ldf.split("\n")
		for x in key_sets:
			key = x.split("=")[0]
			value = x.split(":")[1]
			ldf_dict[key] = value
		return ldf_dict

class LUZ(Serializable):
	def __init__(self, config : dict = None):
		self.config = config

	def serialize(self, stream):
		raise NotImplementedError


	def deserialize(self, stream):
		config = {}
		config["version"] = stream.read(c_ulong)
		if(config["version"] >= 0x24):
			config["ulong_01"] = stream.read(c_ulong)
		config["world_id"] = stream.read(c_ulong)
		if(config["version"] >= 0x26):
			config["spawnpoint_pos"] = Vector3().deserialize(stream)
			config["spawnpoint_rot"] = Vector4().deserialize(stream)
		if(config["version"] < 0x25):
			scene_count = stream.read(c_uint8)
		else:
			scene_count = stream.read(c_ulong)
		config["scenes"] = []
		for _ in range(scene_count):
			scene = {}
			scene["filename"] = String(length_type=c_uint8).deserialize(stream)
			scene["id"] = stream.read(c_uint8)
			scene["scene_3bytes_01"] = stream.read(bytes, length=3)
			scene["is_audio_scene"] = stream.read(c_uint8)
			scene["scene_3bytes_02"] = stream.read(bytes, length=3)
			scene["name"] = String(length_type=c_uint8).deserialize(stream)
			scene["scene_3bytes_03"] = stream.read(bytes, length=3)
			config["scenes"].append(scene)
		config["u8_01"] = stream.read(c_uint8)
		config["terrain_map_filename"] = String(length_type=c_uint8).deserialize(stream)
		config["terrain_map_name"] = String(length_type=c_uint8).deserialize(stream)
		config["terrain_map_desc"] = String(length_type=c_uint8).deserialize(stream)
		if(config["version"] >= 0x20):
			scene_transition_count = stream.read(c_ulong)
			config["scene_transitions"] = []
			for _ in range(scene_transition_count):
				scene_transition = {}
				if(config["version"] < 0x25):
					scene_transition["name"] = (String(length_type=c_uint8).deserialize(stream))
				if(config["version"] <= 0x21 or config["version"] >= 0x27):
					loop_times = 2
				else:
					loop_times = 5
				scene_transition["scene_transition_types"] = []
				for _ in range(loop_times):
					scene_transition_type = {}
					scene_transition_type["scene_id"] = stream.read(c_ulonglong)
					scene_transition_type["transition_point"] = Vector3().deserialize(stream)
					scene_transition["scene_transition_types"].append(scene_transition_type)
				config["scene_transitions"].append(scene_transition)
		config["length_of_rest_of_file"] = stream.read(c_ulong)
		config["ulong_02"] = stream.read(c_ulong)
		path_count = stream.read(c_ulong)
		#TODO: Fix Paths
		# config["paths"] = []
		# for _ in range(path_count):
		# 	path = {}
		# 	path["path_version"] = stream.read(c_ulong)
		# 	path["path_name"] = String(length_type=c_uint8).deserialize(stream)
		# 	path["path_type"] = stream.read(c_ulong)
		# 	path["ulong_01"] = stream.read(c_ulong)
		# 	path["path_behavior"] = stream.read(c_ulong)
		# 	if(path["path_type"] == 1):
		# 		if(path["path_version"] >= 18):
		# 			path["u8_01"] = stream.read(c_uint8)
		# 		elif(path["path_version"] >= 13):
		# 			path["moving_platform_sound"] = stream.read(str, length_type=c_uint8)
		# 	elif(path["path_type"] == 2):
		# 		path["long_01"] = stream.read(c_long)
		# 		path["price"] = stream.read(c_long)
		# 		path["rental_time"] = stream.read(c_long)
		# 		path["accociated_zone"] = stream.read(c_ulonglong)
		# 		path["display_name"] = String(length_type=c_uint8).deserialize(stream)
		# 		path["display_description"] = String(length_type=c_uint8).deserialize(stream)
		# 		path["long_02"] = stream.read(c_long)
		# 		path["clone_limit"] = stream.read(c_long)
		# 		path["reputation_multiplier"] = stream.read(c_float)
		# 		path["rental_time_unit"] = stream.read(c_long)
		# 		path["achievement_required"] = stream.read(c_long)
		# 		path["player_zone_pos"] = Vector3().deserialize(stream)
		# 		path["max_building_height"] = stream.read(c_float)
		# 	elif(path["path_type"] == 3):
		# 		path["next_path"] = String(length_type=c_uint8).deserialize(stream)
		# 		if(path["path_version"] >= 14):
		# 			path["u8_01"] = stream.read(c_uint8)
		# 	elif(path["path_type"] == 4):
		# 		path["spawned_lot"] = stream.read(c_ulong)
		# 		path["respawn_time"] = stream.read(c_ulong)
		# 		path["max_to_spawn"] = stream.read(c_long)
		# 		path["number_to_maintain"] = stream.read(c_ulong)
		# 		path["spawner_object_id"] = stream.read(c_longlong)
		# 		path["activate_spawner_network_on_load"] = stream.read(c_bit)
		# 	waypoint_count = stream.read(c_ulong)
		# 	path["waypoints"] = []
		# 	for _ in range(waypoint_count):
		# 		waypoint = {}
		# 		waypoint["position"] = Vector3().deserialize(stream)
		# 		if(path["path_type"] == 1):
		# 			waypoint["rotation"] = Vector4().deserialize(stream)
		# 			waypoint["lock_player_until_next_waypoint"] = stream.read(c_bit)
		# 			waypoint["speed"] = stream.read(c_float)
		# 			waypoint["wait"] = stream.read(c_float)
		# 			if(path["path_version"] >= 13):
		# 				waypoint["depart_sound"] = stream.read(str, length_type=c_uint8)
		# 				waypoint["arrive_sound"] = stream.read(str, length_type=c_uint8)
		# 		elif(path["path_type"] == 3):
		# 			waypoint["float_01"] = stream.read(c_float)
		# 			waypoint["float_02"] = stream.read(c_float)
		# 			waypoint["float_03"] = stream.read(c_float)
		# 			waypoint["float_04"] = stream.read(c_float)
		# 			waypoint["time"] = stream.read(c_float)
		# 			waypoint["float_05"] = stream.read(c_float)
		# 			waypoint["continuity"] = stream.read(c_float)
		# 			waypoint["bias"] = stream.read(c_float)
		# 		elif(path["path_type"] == 4):
		# 			waypoint["rotation"] = Vector4().deserialize(stream)
		# 		elif(path["path_type"] == 6):
		# 			waypoint["rotation"] = Vector4().deserialize(stream)
		# 			waypoint["u8_01"] = stream.read(c_uint8)
		# 			waypoint["u8_02"] = stream.read(c_uint8)
		# 			waypoint["float_01"] = stream.read(c_float)
		# 			waypoint["float_02"] = stream.read(c_float)
		# 			waypoint["float_03"] = stream.read(c_float)
		# 		elif(path["path_type"] == 7):
		# 			waypoint["float_01"] = stream.read(c_float)
		# 			waypoint["float_02"] = stream.read(c_float)
		# 			waypoint["float_03"] = stream.read(c_float)
		# 			waypoint["float_04"] = stream.read(c_float)
		# 			if(path["path_version"] >= 17):
		# 				waypoint["float_05"] = stream.read(c_float)
		# 		if(path["path_type"] in [0,4,7]):
		# 			waypoint["config"] = {}
		# 			for _ in range(stream.read(c_ulong)):
		# 				waypoint["config"][stream.read(str, length_type=c_uint8)] = stream.read(str, length_type=c_uint8)
		# 		path["waypoints"].append(waypoint)
		# 	config["paths"].append(path)
		return LUZ(config)

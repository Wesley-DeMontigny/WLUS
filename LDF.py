from pyraknet.bitstream import *
from xml.etree import ElementTree
from structures import CString

class LDF():
	def __init__(self):
		self.keys : list = []
	def registerKey(self, KeyName : str, Value : any, Type : int):
		self.keys.append([KeyName, Value, Type])
	def writeLDF(self, Stream : WriteStream):
		keyNum = len(self.keys)
		Stream.write(c_uint(keyNum))
		for key in self.keys:
			name = key[0]
			value = key[1]
			type = key[2]
			Stream.write(c_uint8(len(name) * 2))
			for char in name:
				Stream.write(char.encode('latin1'))
				Stream.write(b'\0')
			Stream.write(c_ubyte(type))
			if(type == 0):
				Stream.write(value, length_type=c_uint)
			elif(type == 1):
				Stream.write(c_int(value))
			elif(type == 3):
				Stream.write(c_float(value))
			elif(type == 5):
				Stream.write(c_uint(value))
			elif(type == 7):
				Stream.write(c_bool(value))
			elif(type == 8 or type == 9):
				Stream.write(c_int64(value))
			elif(type == 13):
				xmlStr = bytes(ElementTree.tostring(value))
				xmlStr = b'<?xml version="1.0">' + xmlStr
				Stream.write(c_ulong(xmlStr.__len__()))
				Stream.write(xmlStr)


#This function is ripped straight from lcdr util
def from_ldf(ldf):
	ldf_dict = {}
	if isinstance(ldf, ReadStream):
		for _ in range(ldf.read(c_uint)):
			key_length = ldf.read(c_ubyte)
			encoded_key = ldf.read(bytes, length=key_length)
			key = encoded_key.decode("utf-16-le")
			data_type_id = ldf.read(c_ubyte)
			if data_type_id == 0:
				value = ldf.read(str, length_type=c_uint)
			elif data_type_id == 1:
				value = ldf.read(c_int)
			elif data_type_id == 3:
				value = ldf.read(c_float)
			elif data_type_id == 5:
				value = ldf.read(c_uint)
			elif data_type_id == 7:
				value = ldf.read(c_bool)
			elif data_type_id in (8, 9):
				value = ldf.read(c_int64)
			elif data_type_id == 13:
				value = ldf.read(bytes, length=ldf.read(c_uint))
			else:
				raise NotImplementedError(key, data_type_id)
			ldf_dict[key] = data_type_id, value
	else:
		pass

	return ldf_dict


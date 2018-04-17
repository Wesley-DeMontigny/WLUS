from bitstream import *

def readOffsetBitstream(data, arg, offset, allocatedLength=33):
	x = BitStream(data[offset:])
	value = x.read(arg, allocated_length=allocatedLength)
	return value

def getFormatName(x):
	if(x == 0):
		return "Variable String"
	if(x == 1):
		return "Signed Long"
	if(x == 2):
		return "Signed Long"
	if(x == 3):
		return "Float"
	if(x == 4):
		return "Double"
	if(x == 5):
		return "Unsigned Long"
	if(x == 6):
		return "Unsigned Long"
	if(x == 7):
		return "Boolean"
	if(x == 8):
		return "Signed Long Long"
	if(x == 9):
		return "Signed Long Long"
	if(x == 13):
		return "XML"
	return "???"

#Most of this is from lcdr util (And by most I mean all, I literally just added a print line so I could see when the function throws an error)
#All I really use it for is for debugging
def from_ldf(ldf):
	ldf_dict = {}
	if isinstance(ldf, BitStream):
		for _ in range(ldf.read(c_uint)):
			encoded_key = ldf.read(bytes, length=ldf.read(c_ubyte))
			key = encoded_key.decode("utf-16-le")
			print("Found Key " + key)
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
		raise NotImplementedError

	return ldf_dict




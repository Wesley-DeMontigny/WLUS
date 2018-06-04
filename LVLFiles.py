from pyraknet.bitstream import *
from structures import Vector3, Vector4

class lvlFile():
	def __init__(self, file):
		self.Objects = []
		self.lvlVersion = 0

		self.parseFile(file)
	def parseFile(self, file):
		lvl = open(file, "rb")
		stream = ReadStream(lvl.read(), unlocked=True)
		try:
			while True:
				buffer = b""
				for i in range(4):
					character = stream.read(bytes, length=1)
					buffer = buffer + character
				if(buffer == b"CHNK"):
					chunkType = stream.read(c_ulong)
					stream.read(c_uint16)
					stream.read(c_uint16)
					stream.read(c_ulong)
					addressofStart = stream.read(c_ulong)
					stream.read(bytes, length=int((addressofStart*8 - int(stream.read_offset))/8))
					if(chunkType == 1000):
						self.lvlVersion = stream.read(c_ulong)
						stream.read(c_ulong)
						stream.read(c_ulong)
						stream.read(c_ulong)
						stream.read(c_ulong)
					elif(chunkType == 2001):
						numOfObjects = stream.read(c_ulong)
						for i in range(numOfObjects):
							gameObj = {}
							gameObj["ObjectID"] = stream.read(c_ulonglong)
							LOT = stream.read(c_ulong)#LOT
							gameObj["LOT"] = (LOT)
							if(self.lvlVersion >= 0x26):
								stream.read(c_ulong)
							if(self.lvlVersion >= 0x20):
								stream.read(c_ulong)
							XPos = (stream.read(c_float))#
							YPos = (stream.read(c_float))
							ZPos = (stream.read(c_float))
							gameObj["Position"] = Vector3(XPos, YPos, ZPos)
							WRot = stream.read(c_float)
							XRot = (stream.read(c_float))
							YRot = (stream.read(c_float))
							ZRot = (stream.read(c_float))
							gameObj["Rotation"] = Vector4(XRot, YRot, ZRot, WRot)
							gameObj["Scale"] = (stream.read(c_float))#Scale
							gameObj["LDF"] = self.readLDF(stream.read(str, length_type=c_ulong))
							if(self.lvlVersion >= 7):
								stream.read(c_ulong)
							self.Objects.append(gameObj)
						break
		except:
			pass

	def readLDF(self, ldf):
		ldf_dict = {}
		keySets = ldf.split("\n")
		for x in keySets:
			key = x.split("=")[0]
			value = x.split(":")[1]
			ldf_dict[key] = value
		return ldf_dict





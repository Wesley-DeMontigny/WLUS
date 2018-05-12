from bitstream import *
from LDFReader import *

class lvlFile():
	def __init__(self, file, zoneID):
		self.Objects = []
		self.lvlVersion = 0
		self.zoneID = zoneID

		self.parseFile(file)
	def parseFile(self, file):
		lvl = open(file, "rb")
		stream = BitStream()
		stream.write(lvl.read())
		while True:
			buffer = ""
			for i in range(4):
				character = stream.read(str, allocated_length=1, char_size=1)
				buffer = buffer + str(character)
			if(buffer == "CHNK"):
				chunkType = stream.read(c_ulong)
				print("Found CHNK Type " + str(chunkType))
				stream.read(c_uint16)
				stream.read(c_uint16)
				stream.read(c_ulong)
				addressofStart = stream.read(c_ulong)
				stream.read_bits(addressofStart*8 - int(stream._read_offset))
				if(chunkType == 1000):
					self.lvlVersion = stream.read(c_ulong)
					stream.read(c_ulong)
					stream.read(c_ulong)
					stream.read(c_ulong)
					stream.read(c_ulong)
				elif(chunkType == 2001):
					print("Parsing Chunk Type 2001")
					numOfObjects = stream.read(c_ulong)
					for i in range(numOfObjects):
						gameObj = {}
						gameObj["ObjectID"] = stream.read(c_ulonglong)
						LOT = stream.read(c_ulong)#LOT
						gameObj["LOT"] = (LOT)
						gameObj["Zone"] = (self.zoneID)
						if(self.lvlVersion >= 0x26):
							stream.read(c_ulong)
						if(self.lvlVersion >= 0x20):
							stream.read(c_ulong)
						gameObj["XPos"] = (stream.read(c_float))#XPos
						gameObj["YPos"] = (stream.read(c_float))#YPos
						gameObj["ZPos"] = (stream.read(c_float))#ZPos
						wRot = stream.read(c_float)
						gameObj["XRot"] = (stream.read(c_float))#XRot
						gameObj["YRot"] = (stream.read(c_float))#YRot
						gameObj["ZRot"] = (stream.read(c_float))#ZRot
						gameObj["WRot"] = (wRot)
						gameObj["Scale"] = (stream.read(c_float))#Scale
						gameObj["LDF"] = from_lvlLDF(stream.read(str, length_type=c_ulong))
						if(self.lvlVersion >= 7):
							stream.read(c_ulong)
						self.Objects.append(gameObj)
					print("Retrieved All Objects From Chunk")
					break

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
						gameObj = []
						stream.read(c_ulonglong)#ObjectID
						LOT = stream.read(c_ulong)#LOT
						gameObj.append(LOT)
						gameObj.append(self.zoneID)
						if(self.lvlVersion >= 0x26):
							stream.read(c_ulong)
						if(self.lvlVersion >= 0x20):
							stream.read(c_ulong)
						gameObj.append(stream.read(c_float))#XPos
						gameObj.append(stream.read(c_float))#YPos
						gameObj.append(stream.read(c_float))#ZPos
						wRot = stream.read(c_float)
						gameObj.append(stream.read(c_float))#XRot
						gameObj.append(stream.read(c_float))#YRot
						gameObj.append(stream.read(c_float))#ZRot
						gameObj.append(wRot)
						gameObj.append(stream.read(c_float))#Scale
						LDF = stream.read(str, length_type=c_ulong)
						if(self.lvlVersion >= 7):
							stream.read(c_ulong)
						self.Objects.append(gameObj)
					print("Retrieved All Objects From Chunk")
					break

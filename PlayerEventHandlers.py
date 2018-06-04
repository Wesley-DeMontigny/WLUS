from pyraknet.bitstream import *
from pyraknet.messages import Address
from core import GameServer
from time import sleep
from structures import Vector3, Vector4

def RemoveHealth(Object, stream : ReadStream, address : Address, Server : GameServer):
	Object.ObjectConfig["Health"] = 0

def Ressurect(Object, stream : ReadStream, address : Address, Server : GameServer):
	packet = WriteStream()
	Server.InitializeGameMessage(packet, Object.ObjectConfig["ObjectID"], 0x00a0)
	Object.ObjectConfig["Health"] = Object.ObjectConfig["MaxHealth"]
	Object.ObjectConfig["Armor"] = Object.ObjectConfig["MaxArmor"]
	Server.brodcastPacket(packet, Object.Zone)
	Object.ObjectConfig["Alive"] = True

def PlayerLoaded(Object, stream : ReadStream, address : Address, Server : GameServer):
	sleep(1.5)
	Object.ObjectConfig["Alive"] = True
	Object.ObjectConfig["LoadingIn"] = False

def RunCommand(Object, stream : ReadStream, address : Address, Server : GameServer):
	if(Object.Parent.IsAdmin == True):
		clientState = stream.read(c_int)
		command = stream.read(str, length_type=c_ulong)
		try:
			args = command.split(" ")
			if(args[0] == "/loadWorld"):
				Server.LoadWorld(Object, int(args[1]), address, SpawnAtDefault = True)
			elif(args[0] == "/fly"):
				packet = WriteStream()
				Server.InitializeGameMessage(packet, Object.ObjectConfig["ObjectID"], 0x0231)
				packet.write(c_bit(True))
				packet.write(c_bit(False))
				packet.write(c_bit(True))
				packet.write(c_int(-1))#EffectID
				packet.write(c_float(10))#Air Speed
				packet.write(c_float(15))#Max Air Speed
				packet.write(c_float(1.5))#Vertical Velocity
				packet.write(c_int(0))
				Server.brodcastPacket(packet, Object.Zone)
			elif(args[0] == "/setConfig"):
				if(Object.ObjectConfig[args[1]] is not None):
					configType = type(Object.ObjectConfig[str(args[1])])
					if(configType == str):
						Object.ObjectConfig[str(args[1])] = str(args[2])
						print("Changed {} to {}".format(args[1], args[2]))
					elif(configType == int):
						Object.ObjectConfig[str(args[1])] = int(args[2])
						print("Changed {} to {}".format(args[1], args[2]))
					elif(configType == Vector3):
						Object.ObjectConfig[str(args[1])] = Vector3(float(args[2]), float(args[3]), float(args[4]))
						print("Changed {} to ({}, {}, {})".format(args[1], args[2], args[3], args[4]))
					elif(configType == Vector4):
						Object.ObjectConfig[str(args[1])] = Vector4(float(args[2]), float(args[3]), float(args[4]), float(args[5]))
						print("Changed {} to ({}, {}, {}, {})".format(args[1], args[2], args[3], args[4], args[5]))
			elif(args[0] == "/spawnObject"):
				Server.spawnObject(int(args[1]), Object.Zone, {}, Position=Object.ObjectConfig["Position"])
			# elif(args[0] == "/addItem"):
			# 	Server.addItemToInventory(int(args[1]), Object, Linked=1)
		except:
			pass
	else:
		print("{} Is Not An Admin!".format(Object.ObjectConfig("Name")))


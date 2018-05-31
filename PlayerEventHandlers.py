from pyraknet.bitstream import *
from pyraknet.messages import Address
from core import GameServer
from time import sleep

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

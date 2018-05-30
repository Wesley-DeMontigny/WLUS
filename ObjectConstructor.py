from pyraknet.bitstream import *
from ReplicaComponents import *
from Enum import ReplicaTypes


def WriteReplica(stream : WriteStream, ComponentList : list, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	writeBaseData(stream, ObjectConfig, ReplicaType)

	if(108 in ComponentList):
		print("Component 108 Is Not Implemented!")
		return
	if(61 in ComponentList):
		print("Module Assembly Is Not Implemented!")
		return
	if(1 in ComponentList):
		writeControllablePhysics(stream, ObjectConfig, ReplicaType)
	if(3 in ComponentList):
		print("Simple Physics Is Not Implemented!")
		return
	if(20 in ComponentList):
		print("Rigidbody Physics Is Not Implemented!")
		return
	if(30 in ComponentList):
		print("Vehicle Physics Is Not Implemented!")
		return
	if(40 in ComponentList):
		print("Phantom Physics Is Not Implemented!")
		return
	if(7 in ComponentList):
		writeDestructible(stream, ObjectConfig, ReplicaType)
	if(23 in ComponentList):
		print("Collectible Is Not Implemented!")
		return
	if(26 in ComponentList):
		print("Pet Is Not Implemented!")
		return
	if(4 in ComponentList):
		writeCharacter(stream, ObjectConfig, ReplicaType)
	if(19 in ComponentList):
		print("Shooting Gallery Is Not Implemented!")
		return
	if(17 in ComponentList):
		writeInventory(stream, ObjectConfig, ReplicaType)
	if(5 in ComponentList):
		writeScript(stream, ObjectConfig, ReplicaType)
	if(9 in ComponentList):
		writeSkill(stream, ObjectConfig, ReplicaType)
	if(60 in ComponentList):
		print("Base Combat AI Is Not Implemented!")
		return
	if(48 in ComponentList):
		print("Rebuild Is Not Implemented!")
		return
	if(25 in ComponentList):
		print("Moving Platform Is Not Implemented!")
		return
	if(49 in ComponentList):
		print("Switch Is Not Implemented!")
		return
	if(16 in ComponentList):
		print("Vendor Is Not Implemented!")
		return
	if(6 in ComponentList):
		print("Bouncer Is Not Implemented!")
		return
	if(39 in ComponentList):
		print("Scripted Activity Is Not Implemented!")
		return
	if(71 in ComponentList):
		print("Racing Control Is Not Implemented!")
		return
	if(75 in ComponentList):
		print("LUP Exhibit Is Not Implemented!")
		return
	if(2 in ComponentList):
		writeRender(stream, ObjectConfig, ReplicaType)
	if(107 in ComponentList):
		writeComponent107(stream, ObjectConfig, ReplicaType)
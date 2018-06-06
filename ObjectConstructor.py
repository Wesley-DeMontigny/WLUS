from pyraknet.bitstream import *
from ReplicaComponents import *
from Enum import ReplicaTypes


def WriteReplica(stream : WriteStream, ComponentList : list, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	writeBaseData(stream, ObjectConfig, ReplicaType)

	if(108 in ComponentList):
		writeComponent108(stream, ObjectConfig, ReplicaType)
	if(61 in ComponentList):
		writeModuleAssembly(stream, ObjectConfig, ReplicaType)
	if(1 in ComponentList):
		writeControllablePhysics(stream, ObjectConfig, ReplicaType)
	if(3 in ComponentList):
		writeSimplePhysics(stream, ObjectConfig, ReplicaType)
	if(20 in ComponentList):
		writeRigibbodyPhantomPhysics(stream, ObjectConfig, ReplicaType)
	if(30 in ComponentList):
		writeVehiclePhysics(stream, ObjectConfig, ReplicaType)
	if(40 in ComponentList):
		writePhantomPhysics(stream, ObjectConfig, ReplicaType)
	if(7 in ComponentList):
		writeDestructible(stream, ObjectConfig, ReplicaType)
	if(23 in ComponentList):
		writeCollectible(stream, ObjectConfig, ReplicaType)
	if(26 in ComponentList):
		writePet(stream, ObjectConfig, ReplicaType)
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
		writeBaseCombatAI(stream, ObjectConfig, ReplicaType)
	if(48 in ComponentList):
		writeRebuild(stream, ObjectConfig, ReplicaType)
	if(25 in ComponentList):
		writeMovingPlatform(stream, ObjectConfig, ReplicaType)
	if(49 in ComponentList):
		writeSwitch(stream, ObjectConfig, ReplicaType)
	if(16 in ComponentList):
		writeVendor(stream, ObjectConfig, ReplicaType)
	if(6 in ComponentList):
		writeBouncer(stream, ObjectConfig, ReplicaType)
	if(39 in ComponentList):
		writeScriptedActivity(stream, ObjectConfig, ReplicaType)
	if(71 in ComponentList):
		print("Racing Control Is Not Implemented!")
		return
	if(75 in ComponentList):
		writeExhibit(stream, ObjectConfig, ReplicaType)
	if(2 in ComponentList):
		if("Render" not in ObjectConfig or ObjectConfig["Render"] == True):
			writeRender(stream, ObjectConfig, ReplicaType)
	if(107 in ComponentList):
		writeComponent107(stream, ObjectConfig, ReplicaType)
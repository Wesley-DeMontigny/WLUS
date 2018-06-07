from pyraknet.bitstream import *
from Enum import ReplicaTypes
from structures import *


def writeBaseData(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_longlong(ObjectConfig["ObjectID"]))
		stream.write(c_long(ObjectConfig["LOT"]))
		stream.write(ObjectConfig["Name"], length_type=c_uint8)
		stream.write(c_ulong(0))  # Time since created
		stream.write(c_bit(False))  # Model flag?? TODO : Implement this later
		stream.write(c_bit(False))  # Trigger ID
		if (ObjectConfig["SpawnerID"] != None):
			stream.write(c_bit(True))
			stream.write(c_longlong(ObjectConfig["SpawnerID"]))
			stream.write(c_bit(True))
			stream.write(c_ulong(0))
		else:
			stream.write(c_bit(False))
			stream.write(c_bit(False))
		stream.write(c_bit(True))
		stream.write(c_float(ObjectConfig["Scale"]))
		stream.write(c_bit(False))
		stream.write(c_bit(False))
	stream.write(c_bit(False))#TODO: Implement Parent/Child Objects Later

def writePet(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(False))

def writeMovingPlatform(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(False))#TODO: Implement
	stream.write(c_bit(False))

def writeControllablePhysics(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))#Jetpack Flag?
		stream.write(c_bit(False))
	stream.write(c_bit(False))
	stream.write(c_bit(False))
	stream.write(c_bit(False))
	stream.write(c_bit(True))
	stream.write(c_float(ObjectConfig["Position"].X))
	stream.write(c_float(ObjectConfig["Position"].Y))
	stream.write(c_float(ObjectConfig["Position"].Z))
	stream.write(c_float(ObjectConfig["Rotation"].X))
	stream.write(c_float(ObjectConfig["Rotation"].Y))
	stream.write(c_float(ObjectConfig["Rotation"].Z))
	stream.write(c_float(ObjectConfig["Rotation"].W))
	if("OnGround" in ObjectConfig):
		stream.write(c_bit(ObjectConfig["OnGround"]))
	else:
		stream.write(c_bit(True))
	stream.write(c_bit(False))
	if("Velocity" in ObjectConfig):
		if(ObjectConfig["Velocity"] != Vector3(0,0,0)):
			stream.write(c_bit(True))
			stream.write(c_float(ObjectConfig["Velocity"].X))
			stream.write(c_float(ObjectConfig["Velocity"].Y))
			stream.write(c_float(ObjectConfig["Velocity"].Z))
		else:
			stream.write(c_bit(False))
	else:
		stream.write(c_bit(False))
	if("AngularVelocity" in ObjectConfig):
		if(ObjectConfig["AngularVelocity"] != Vector3(0,0,0)):
			stream.write(c_bit(True))
			stream.write(c_float(ObjectConfig["AngularVelocity"].X))
			stream.write(c_float(ObjectConfig["AngularVelocity"].Y))
			stream.write(c_float(ObjectConfig["AngularVelocity"].Z))
		else:
			stream.write(c_bit(False))
	else:
		stream.write(c_bit(False))
	stream.write(c_bit(False))#Moving platform flag?
	if(ReplicaType == ReplicaTypes.Serialization):
		stream.write(c_bit(False))

def writeDestructible(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	writeDestructibleIndex(stream, ObjectConfig, ReplicaType)
	writeStatsIndex(stream, ObjectConfig, ReplicaType)

def writeDestructibleIndex(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))#TODO: Implement entire component
		stream.write(c_bit(False))

def writeStatsIndex(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))

	stream.write(c_bit(True))
	if("Health" in ObjectConfig):
		stream.write(c_ulong(ObjectConfig["Health"]))
	else:
		stream.write(c_ulong(1))
	if("MaxHealth" in ObjectConfig):
		stream.write(c_float(ObjectConfig["MaxHealth"]))
	else:
		stream.write(c_float(1))
	if("Armor" in ObjectConfig):
		stream.write(c_ulong(ObjectConfig["Armor"]))
	else:
		stream.write(c_ulong(0))
	if("MaxArmor" in ObjectConfig):
		stream.write(c_float(ObjectConfig["MaxArmor"]))
	else:
		stream.write(c_float(0))
	if("Imagination" in ObjectConfig):
		stream.write(c_ulong(ObjectConfig["Imagination"]))
	else:
		stream.write(c_ulong(0))
	if("MaxImagination" in ObjectConfig):
		stream.write(c_float(ObjectConfig["MaxImagination"]))
	else:
		stream.write(c_float(0))
	stream.write(c_ulong(0))
	stream.write(c_bit(False))
	stream.write(c_bit(False))
	stream.write(c_bit(False))
	if("MaxHealth" in ObjectConfig):
		stream.write(c_float(ObjectConfig["MaxHealth"]))
	else:
		stream.write(c_float(1))
	if("MaxArmor" in ObjectConfig):
		stream.write(c_float(ObjectConfig["MaxArmor"]))
	else:
		stream.write(c_float(0))
	if("MaxImagination" in ObjectConfig):
		stream.write(c_float(ObjectConfig["MaxImagination"]))
	else:
		stream.write(c_float(0))
	stream.write(c_ulong(1))#Count?
	if("Faction" in ObjectConfig):
		stream.write(c_long(ObjectConfig["Faction"]))
	else:
		stream.write(c_long(1))
	if("isSmashable" in ObjectConfig):
		stream.write(c_bit(ObjectConfig["isSmashable"]))
	else:
		stream.write(c_bit(False))

	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))
		stream.write(c_bit(False))
		if("isSmashable" in ObjectConfig):
			if(ObjectConfig["isSmashable"]):
				stream.write(c_bit(False))
				stream.write(c_bit(False))

	stream.write(c_bit(False))

def writeCharacter(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(False))#TODO: Implement with vehicles
	stream.write(c_bit(True))
	stream.write(c_ulong(ObjectConfig["Level"]))
	stream.write(c_bit(False))
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))
		stream.write(c_bit(False))
		stream.write(c_bit(False))
		stream.write(c_bit(False))
		stream.write(c_ulong(ObjectConfig["HairColor"]))
		stream.write(c_ulong(ObjectConfig["HairStyle"]))
		stream.write(c_ulong(0))
		stream.write(c_ulong(ObjectConfig["ShirtColor"]))
		stream.write(c_ulong(ObjectConfig["PantsColor"]))
		stream.write(c_ulong(0))
		stream.write(c_ulong(0))
		stream.write(c_ulong(ObjectConfig["Eyebrows"]))
		stream.write(c_ulong(ObjectConfig["Eyes"]))
		stream.write(c_ulong(ObjectConfig["Mouth"]))
		stream.write(c_ulonglong(ObjectConfig["AccountID"]))
		stream.write(c_ulonglong(0))
		stream.write(c_ulonglong(0))
		stream.write(c_ulonglong(ObjectConfig["UniverseScore"]))
		stream.write(c_bit(False))#Free to play

		Statistics = ObjectConfig["CharacterStatistics"]
		stream.write(c_longlong(Statistics.CurrencyCollected))
		stream.write(c_longlong(Statistics.BricksCollected))
		stream.write(c_longlong(Statistics.SmashablesSmashed))
		stream.write(c_longlong(Statistics.QuickBuildsDone))
		stream.write(c_longlong(Statistics.EnemiesSmashed))
		stream.write(c_longlong(Statistics.RocketsUsed))
		stream.write(c_longlong(len(ObjectConfig["CompletedMissions"])))
		stream.write(c_longlong(Statistics.PetsTamed))
		stream.write(c_longlong(Statistics.ImaginationCollected))
		stream.write(c_longlong(Statistics.HealthCollected))
		stream.write(c_longlong(Statistics.ArmorCollected))
		stream.write(c_longlong(Statistics.DistanceTraveled))
		stream.write(c_longlong(Statistics.TimesDied))
		stream.write(c_longlong(Statistics.DamageTaken))
		stream.write(c_longlong(Statistics.DamageHealed))
		stream.write(c_longlong(Statistics.ArmorRepaired))
		stream.write(c_longlong(Statistics.ImaginationRestored))
		stream.write(c_longlong(Statistics.ImaginationUsed))
		stream.write(c_longlong(Statistics.DistanceDriven))
		stream.write(c_longlong(Statistics.TimeAirborneInCar))
		stream.write(c_longlong(Statistics.RacingImaginationCollected))
		stream.write(c_longlong(Statistics.RacingImaginationCratesSmashed))
		stream.write(c_longlong(Statistics.RaceCarBoosts))
		stream.write(c_longlong(Statistics.CarWrecks))
		stream.write(c_longlong(Statistics.RacingSmashablesSmashed))
		stream.write(c_longlong(Statistics.RacesFinished))
		stream.write(c_longlong(Statistics.RacesWon))

		stream.write(c_bit(False))
		stream.write(c_bit(False))#Landing by rocket

	stream.write(c_bit(True))#TODO: Implement this branch enventually
	stream.write(c_bit(ObjectConfig["PVPEnabled"]))
	stream.write(c_bit(False))
	stream.write(c_uint8(0))
	stream.write(c_bit(False))
	stream.write(c_uint8(0))

	stream.write(c_bit(False))
	stream.write(c_bit(False))#TODO: Implement Guilds

def writeInventory(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if("Inventory" in ObjectConfig):
		inventory = ObjectConfig["Inventory"]
		equipped = inventory.getEquippedItems()
		stream.write(c_bit(True))
		stream.write(c_ulong(len(equipped)))
		for item in equipped:
			stream.write(c_longlong(item["ObjectID"]))
			stream.write(c_long(item["LOT"]))
			stream.write(c_bit(False))
			stream.write(c_bit(True))
			stream.write(c_ulong(item["Quantity"]))
			stream.write(c_bit(True))
			stream.write(c_uint16(item["Slot"]))
			stream.write(c_bit(False))
			stream.write(c_bit(False))#TODO: Implement later
			stream.write(c_bit(True))
	else:
		stream.write(c_bit(False))
	stream.write(c_bit(False))

def writeScript(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))#TODO: Implement, what do the docs mean by same "structure as chardata packet"?

def writeSkill(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))#TODO: Figure this out and implement it

def writeRender(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_ulong(0))#TODO: Figure this out and implement it

def writeComponent107(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(False))

def writeBouncer(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(True))
	if("petNotRequired" in ObjectConfig):
		stream.write(c_bit(ObjectConfig["petNotRequired"]))
	else:
		stream.write(c_bit(False))

def writeRigibbodyPhantomPhysics(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(True))
	stream.write(c_float(ObjectConfig["Position"].X))
	stream.write(c_float(ObjectConfig["Position"].Y))
	stream.write(c_float(ObjectConfig["Position"].Z))
	stream.write(c_float(ObjectConfig["Rotation"].X))
	stream.write(c_float(ObjectConfig["Rotation"].Y))
	stream.write(c_float(ObjectConfig["Rotation"].Z))
	stream.write(c_float(ObjectConfig["Rotation"].W))

def writeComponent108(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(False))#TODO: Implement this

def writeVendor(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(True))
	stream.write(c_bit(False))
	stream.write(c_bit(False))

def writeSimplePhysics(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))
		stream.write(c_float(0))
	stream.write(c_bit(False))
	stream.write(c_bit(False))
	stream.write(c_bit(True))
	stream.write(c_float(ObjectConfig["Position"].X))
	stream.write(c_float(ObjectConfig["Position"].Y))
	stream.write(c_float(ObjectConfig["Position"].Z))
	stream.write(c_float(ObjectConfig["Rotation"].X))
	stream.write(c_float(ObjectConfig["Rotation"].Y))
	stream.write(c_float(ObjectConfig["Rotation"].Z))
	stream.write(c_float(ObjectConfig["Rotation"].W))

def writeVehiclePhysics(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_uint8(0))
		stream.write(c_bit(False))
	stream.write(c_bit(False))

def writeSwitch(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if("SwitchState" in ObjectConfig):
		stream.write(c_bit(ObjectConfig["SwitchState"]))
	else:
		stream.write(c_bit(False))

def writeBaseCombatAI(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(True))
	if("AIActionState" in ObjectConfig):
		stream.write(c_ulong(ObjectConfig["AIActionState"]))
	else:
		stream.write(c_ulong(0))
	if("TargetObject" in ObjectConfig):
		stream.write(c_longlong(ObjectConfig["TargetObject"]))
	else:
		stream.write(c_longlong(0))

def writePhantomPhysics(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(True))
	stream.write(c_float(ObjectConfig["Position"].X))
	stream.write(c_float(ObjectConfig["Position"].Y))
	stream.write(c_float(ObjectConfig["Position"].Z))
	stream.write(c_float(ObjectConfig["Rotation"].X))
	stream.write(c_float(ObjectConfig["Rotation"].Y))
	stream.write(c_float(ObjectConfig["Rotation"].Z))
	stream.write(c_float(ObjectConfig["Rotation"].W))
	stream.write(c_bit(False))#TODO: Implement Physics Effects

def writeExhibit(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(True))
	if("ExhibitedLOT" in ObjectConfig):
		stream.write(c_long(ObjectConfig["ExhibitedLOT"]))
	else:
		stream.write(c_long(45))

def writeScriptedActivity(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	stream.write(c_bit(False))#TODO: Implement this

def writeRebuildIndex(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	writeScriptedActivity(stream, ObjectConfig, ReplicaType)
	stream.write(c_bit(True))
	if("RebuildState" in ObjectConfig):
		stream.write(c_ulong(ObjectConfig["RebuildState"]))
	else:
		stream.write(c_ulong(0))
	if("RebuildSuccess" in ObjectConfig):
		stream.write(c_bit(ObjectConfig["RebuildSuccess"]))
	else:
		stream.write(c_bit(False))
	if("RebuildEnabled" in ObjectConfig):
		stream.write(c_bit(ObjectConfig["RebuildEnabled"]))
	else:
		stream.write(c_bit(True))
	stream.write(c_float(0))#Time since start of rebuild
	stream.write(c_float(0))
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))
		if("BuildActivatorPos" in ObjectConfig):
			stream.write(c_float(ObjectConfig["BuildActivatorPos"].X))
			stream.write(c_float(ObjectConfig["BuildActivatorPos"].Y))
			stream.write(c_float(ObjectConfig["BuildActivatorPos"].Z))
		else:
			stream.write(c_float(ObjectConfig["Position"].X))
			stream.write(c_float(ObjectConfig["Position"].Y))
			stream.write(c_float(ObjectConfig["Position"].Z))
		stream.write(c_bit(False))

def writeModuleAssembly(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))#TODO: Implement

def writeCollectible(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	writeStatsIndex(stream, ObjectConfig, ReplicaType)
	writeCollectibleIndex(stream, ObjectConfig, ReplicaType)

def writeRebuild(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	writeStatsIndex(stream, ObjectConfig, ReplicaType)
	writeRebuildIndex(stream, ObjectConfig, ReplicaType)

def writeCollectibleIndex(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if("CollectibleID" in ObjectConfig):
		stream.write(c_uint16(ObjectConfig["CollectibleID"]))
	else:
		stream.write(c_uint16(0))






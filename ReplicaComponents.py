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
	stream.write(c_bit(ObjectConfig["OnGround"]))
	stream.write(c_bit(False))
	if(ObjectConfig["Velocity"] != Vector3(0,0,0)):
		stream.write(c_bit(True))
		stream.write(c_float(ObjectConfig["Velocity"].X))
		stream.write(c_float(ObjectConfig["Velocity"].Y))
		stream.write(c_float(ObjectConfig["Velocity"].Z))
	else:
		stream.write(c_bit(False))
	if(ObjectConfig["AngularVelocity"] != Vector3(0,0,0)):
		stream.write(c_bit(True))
		stream.write(c_float(ObjectConfig["AngularVelocity"].X))
		stream.write(c_float(ObjectConfig["AngularVelocity"].Y))
		stream.write(c_float(ObjectConfig["AngularVelocity"].Z))
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

def writeStatsIndex(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))

	stream.write(c_bit(True))
	stream.write(c_ulong(ObjectConfig["Health"]))
	stream.write(c_float(ObjectConfig["MaxHealth"]))
	stream.write(c_ulong(ObjectConfig["Armor"]))
	stream.write(c_float(ObjectConfig["MaxArmor"]))
	stream.write(c_ulong(ObjectConfig["Imagination"]))
	stream.write(c_float(ObjectConfig["MaxImagination"]))
	stream.write(c_ulong(0))
	stream.write(c_bit(False))
	stream.write(c_bit(False))
	stream.write(c_bit(False))
	stream.write(c_float(ObjectConfig["MaxHealth"]))
	stream.write(c_float(ObjectConfig["MaxArmor"]))
	stream.write(c_float(ObjectConfig["MaxImagination"]))
	stream.write(c_ulong(1))#Count?
	stream.write(c_long(ObjectConfig["Faction"]))
	stream.write(c_bit(ObjectConfig["isSmashable"]))

	if(ReplicaType == ReplicaTypes.Construction):
		stream.write(c_bit(False))
		stream.write(c_bit(False))
		stream.write(c_bit(ObjectConfig["isSmashable"]))
		if(ObjectConfig["isSmashable"]):
			stream.write(c_bit(False))
			stream.write(c_bit(False))

	stream.write(c_bit(False))

def writeCharacter(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
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

		Statistics : CharacterStatistics = ObjectConfig["CharacterStatistics"]
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

	stream.write(c_bit(False))#TODO: Implement this branch enventually

	stream.write(False)
	stream.write(False)#TODO: Implement Guilds

def writeInventory(stream : WriteStream, ObjectConfig : dict, ReplicaType : ReplicaTypes):
	inventory : Inventory = ObjectConfig["Inventory"]
	stream.write(c_bit(True))
	stream.write(c_ulong(len(inventory.InventoryList)))
	for item in inventory.InventoryList:
		stream.write(c_longlong(item["ObjectID"]))
		stream.write(c_long(item["LOT"]))
		stream.write(c_bit(False))
		stream.write(c_bit(True))
		stream.write(c_ulong(item["Quantity"]))
		stream.write(c_bit(True))
		stream.write(c_uint16(item["Slot"]))
		stream.write(c_bit(False))
		stream.write(c_bit(False))#TODO: Implement later
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





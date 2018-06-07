from pyraknet.bitstream import *
from pyraknet.messages import Address
from core import GameServer

def PlatformResync(Object, stream : ReadStream, address : Address, Server : GameServer):
	packet = WriteStream()
	Server.InitializeGameMessage(packet, Object.ObjectConfig["ObjectID"], 0x02f9)
	Server.send(packet, address)

def MissionOffering(Object, stream : ReadStream, address : Address, Server : GameServer):
	Complete = stream.read(c_bit)
	State = stream.read(c_int)
	MissionID = stream.read(c_int)
	PlayerID = stream.read(c_longlong)

	taskTable = Server.CDClient.Tables["MissionTasks"]
	task = taskTable.select(["taskType"], "id = {}".format(MissionID))[0]["taskType"]

	MissionTask = WriteStream()
	Server.InitializeGameMessage(MissionTask, PlayerID, 0x0ff)
	MissionTask.write(c_int(MissionID))
	MissionTask.write(c_int(1 << (task + 1)))
	MissionTask.write(c_uint8(0))
	Server.send(MissionTask, address)

	NotifyMission = WriteStream()
	Server.InitializeGameMessage(NotifyMission, PlayerID, 0x0fe)
	NotifyMission.write(c_int(MissionID))
	if(Complete == False):
		NotifyMission.write(c_int(State))
	else:
		NotifyMission.write(c_int(8))
	NotifyMission.write(c_bit(False))
	Server.send(NotifyMission, address)

	if(Server.Game.getObjectByID(PlayerID).getMissionByID(MissionID) is None):
		missionTable = Server.CDClient.Tables["Missions"]
		mission = missionTable.select(["target_objectID", "id", "defined_type",
										"prereqMissionID", "reward_currency",
										"LegoScore", "reward_item1", "reward_item1_count",
										"reward_item2", "reward_item2_count", "reward_item3",
										"reward_item3_count", "reward_item4", "reward_item4_count", "offer_objectID"],
									   "id = {}".format(MissionID))[0]
		Server.Game.getObjectByID(PlayerID).giveMission(mission, task)
	else:
		player = Server.Game.getObjectByID(PlayerID)
		missionObj = player.getMissionByID(MissionID)
		missionObj.Complete()
		missionObj.Parent.ObjectConfig["CompletedMissions"].append(MissionID)
		print(missionObj.Parent.ObjectConfig["CompletedMissions"])
		for i in range(len(missionObj.Parent.ObjectConfig["CurrentMissions"])):
			if(missionObj.Parent.ObjectConfig["CurrentMissions"][i] == missionObj):
				del missionObj.Parent.ObjectConfig["CurrentMissions"][i]
				print("Removed Old Mission")
				break

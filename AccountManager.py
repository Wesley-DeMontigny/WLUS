from passlib.hash import sha256_crypt
from GameManager import Character, CharacterStatistics, Inventory, Mission
from GameDB import *
from structures import Vector3, Vector4
from ServerUtilities import getPantsID, getShirtID
import random

class AccountManager():
	def __init__(self):
		self.Accounts = []

	def registerAccountToClient(self, Username: str, Password: str, IsAdmin : bool = False):
		account = Account(self)
		account.Username = Username
		account.Password = sha256_crypt.encrypt(Password)
		account.IsAdmin = IsAdmin
		account.AccountID = len(self.Accounts) + 1
		account.Banned = False
		self.Accounts.append(account)

	def registerAccountToDB(self, Username: str, Password: str, IsAdmin : bool, DB : GameDB):
		if(DB.Tables["Accounts"].select(["AccountID"], "Username = {}".format(Username)) != []):
			DB.Tables["Accounts"].insert({"Username":Username, "Password":sha256_crypt.encrypt(Password), "IsAdmin":int(IsAdmin), "Banned":0})
			return True
		else:
			return False

	def registerAccount(self, Username: str, Password: str, IsAdmin : bool, DB : GameDB):
		result = self.registerAccountToDB(Username, Password, IsAdmin, DB)
		if(result == True):
			print("Registered Account")


	def getAccountByUsername(self, Username: str):
		for Account in self.Accounts:
			if (Account.Username == Username):
				return Account
		return None

	def getCharacterByObjectID(self, ObjectID : int):
		for Account in self.Accounts:
			for Character in Account.Characters:
				if(Character.ObjectConfig["ObjectID"] == ObjectID):
					return Character
		return None

	def Save(self, Server : GameDB):
		CharacterTable : DBTable = Server.Tables["Characters"]
		CharacterStats : DBTable = Server.Tables["CharacterStatistics"]
		CompMissionTable : DBTable = Server.Tables["CompletedMissions"]
		CurrentMissionsTable: DBTable = Server.Tables["CurrentMissions"]
		InventoryTable: DBTable = Server.Tables["Inventory"]
		CharacterConfigTable : DBTable = Server.Tables["CharacterConfig"]

		for account in self.Accounts:
			for character in account.Characters:
				if(CharacterTable.select(["Name"], "ObjectID = {}".format(character.ObjectConfig["ObjectID"])) != []):
					#print("Updated Character {}".format(character.ObjectConfig["ObjectID"]))
					CharacterTable.update({"Name":character.ObjectConfig["Name"], "Zone":character.Zone}, "ObjectID = {} AND AccountID = {}".format(character.ObjectConfig["ObjectID"], account.AccountID))

					Stats : CharacterStats = character.ObjectConfig["CharacterStatistics"]
					CharacterStats.update({"CurrencyCollected":Stats.CurrencyCollected,
										   "BricksCollected": Stats.BricksCollected,
										   "SmashablesSmashed": Stats.SmashablesSmashed,
										   "QuickBuildsDone": Stats.QuickBuildsDone,
										   "EnemiesSmashed": Stats.EnemiesSmashed,
										   "RocketsUsed": Stats.RocketsUsed,
										   "PetsTamed": Stats.PetsTamed,
										   "ImaginationCollected": Stats.ImaginationCollected,
										   "HealthCollected": Stats.HealthCollected,
										   "ArmorCollected": Stats.ArmorCollected,
										   "DistanceTraveled": Stats.DistanceTraveled,
										   "TimesDied": Stats.TimesDied,
										   "DamageTaken": Stats.DamageTaken,
										   "DamageHealed": Stats.DamageHealed,
										   "ArmorRepaired": Stats.ArmorRepaired,
										   "ImaginationRestored": Stats.ImaginationRestored,
										   "ImaginationUsed": Stats.ImaginationUsed,
										   "DistanceDriven": Stats.DistanceDriven,
										   "TimeAirborneInCar": Stats.TimeAirborneInCar,
										   "RacingImaginationCollected": Stats.RacingImaginationCollected,
										   "RacingImaginationCratesSmashed": Stats.RacingImaginationCratesSmashed,
										   "RaceCarBoosts": Stats.RaceCarBoosts,
										   "CarWrecks": Stats.CarWrecks,
										   "RacingSmashablesSmashed": Stats.RacingSmashablesSmashed,
										   "RacesFinished": Stats.RacesFinished,
										   "RacesWon": Stats.RacesWon}, "PlayerID = {}".format(character.ObjectConfig["ObjectID"]))

					CompMissionTable.delete("PlayerID = {}".format(character.ObjectConfig["ObjectID"]))
					for mission in character.ObjectConfig["CompletedMissions"]:
						CompMissionTable.insert({"PlayerID":character.ObjectConfig["ObjectID"], "MissionID":mission})

					CurrentMissionsTable.delete("PlayerID = {}".format(character.ObjectConfig["ObjectID"]))
					for mission in character.ObjectConfig["CurrentMissions"]:
						rewardItems = ""
						for x in range(len(mission.RewardItems)):
							if(x != len(mission.RewardItems)-1):
								rewardItems += str(mission.RewardItems[x]) + "|"
							else:
								rewardItems += str(mission.RewardItems[x])
						CurrentMissionsTable.insert({"PlayerID":character.ObjectConfig["ObjectID"],
													 "MissionType":mission.MissionType,
													 "RewardCurrency":mission.RewardCurrency,
													 "RewardItems":rewardItems,
													 "RewardUniverseScore":mission.RewardUniverseScore,
													 "Offerer":mission.Offerer,
													 "Target":mission.Target,
													 "Progress":mission.Progress})

					InventoryTable.delete("OwnerID = {}".format(character.ObjectConfig["ObjectID"]))
					inventory : Inventory = character.ObjectConfig["Inventory"]
					for item in inventory.InventoryList:
						InventoryTable.insert({"LOT":item["LOT"], "Slot":item["Slot"],
											   "Equipped":int(item["Equipped"]), "Linked":int(item["Linked"]),
											   "Quantity":item["Quantity"], "ObjectID":item["ObjectID"],
											   "OwnerID":character.ObjectConfig["ObjectID"]})

					posStr = "{},{},{}".format(character.ObjectConfig["Position"].X,character.ObjectConfig["Position"].Y,character.ObjectConfig["Position"].Z)
					rotStr = "{},{},{},{}".format(character.ObjectConfig["Rotation"].X,
											   character.ObjectConfig["Rotation"].Y,
											   character.ObjectConfig["Rotation"].Z,
												character.ObjectConfig["Rotation"].W)

					CharacterConfigTable.update({"UniverseScore":character.ObjectConfig["UniverseScore"],
												 "Level":character.ObjectConfig["Level"],
												 "Health":character.ObjectConfig["Health"],
												 "MaxHealth":character.ObjectConfig["MaxHealth"],
												 "Armor":character.ObjectConfig["Armor"],
												 "MaxArmor": character.ObjectConfig["MaxArmor"],
												 "Imagination": character.ObjectConfig["Imagination"],
												 "MaxImagination": character.ObjectConfig["MaxImagination"],
												 "Currency": character.ObjectConfig["Currency"],
												 "Position":posStr,
												 "Rotation":rotStr}, "PlayerID = {}".format(character.ObjectConfig["ObjectID"]))
				else:
					#print("Inserted Character {}".format(character.ObjectConfig["ObjectID"]))
					CharacterTable.insert({"ObjectID":character.ObjectConfig["ObjectID"], "Name":character.ObjectConfig["Name"],
					"Zone":character.Zone, "ShirtColor":character.ObjectConfig["ShirtColor"], "ShirtStyle":character.ObjectConfig["ShirtStyle"],
					"PantsColor":character.ObjectConfig["PantsColor"], "HairColor":character.ObjectConfig["HairColor"], "HairStyle":character.ObjectConfig["HairStyle"],
					"lh":character.ObjectConfig["lh"], "rh":character.ObjectConfig["rh"], "Eyebrows":character.ObjectConfig["Eyebrows"],
					"Eyes":character.ObjectConfig["Eyes"], "Mouth":character.ObjectConfig["Mouth"], "AccountID":account.AccountID})

					Stats : CharacterStats = character.ObjectConfig["CharacterStatistics"]
					CharacterStats.insert({"PlayerID":character.ObjectConfig["ObjectID"],
										   "CurrencyCollected":Stats.CurrencyCollected,
										   "BricksCollected": Stats.BricksCollected,
										   "SmashablesSmashed": Stats.SmashablesSmashed,
										   "QuickBuildsDone": Stats.QuickBuildsDone,
										   "EnemiesSmashed": Stats.EnemiesSmashed,
										   "RocketsUsed": Stats.RocketsUsed,
										   "PetsTamed": Stats.PetsTamed,
										   "ImaginationCollected": Stats.ImaginationCollected,
										   "HealthCollected": Stats.HealthCollected,
										   "ArmorCollected": Stats.ArmorCollected,
										   "DistanceTraveled": Stats.DistanceTraveled,
										   "TimesDied": Stats.TimesDied,
										   "DamageTaken": Stats.DamageTaken,
										   "DamageHealed": Stats.DamageHealed,
										   "ArmorRepaired": Stats.ArmorRepaired,
										   "ImaginationRestored": Stats.ImaginationRestored,
										   "ImaginationUsed": Stats.ImaginationUsed,
										   "DistanceDriven": Stats.DistanceDriven,
										   "TimeAirborneInCar": Stats.TimeAirborneInCar,
										   "RacingImaginationCollected": Stats.RacingImaginationCollected,
										   "RacingImaginationCratesSmashed": Stats.RacingImaginationCratesSmashed,
										   "RaceCarBoosts": Stats.RaceCarBoosts,
										   "CarWrecks": Stats.CarWrecks,
										   "RacingSmashablesSmashed": Stats.RacingSmashablesSmashed,
										   "RacesFinished": Stats.RacesFinished,
										   "RacesWon": Stats.RacesWon})

					for mission in character.ObjectConfig["CompletedMissions"]:
						CompMissionTable.insert({"PlayerID":character.ObjectConfig["ObjectID"], "MissionID":mission})

					for mission in character.ObjectConfig["CurrentMissions"]:
						rewardItems = ""
						for x in range(len(mission.RewardItems)):
							if(x != len(mission.RewardItems)-1):
								rewardItems += str(mission.RewardItems[x]) + "|"
							else:
								rewardItems += str(mission.RewardItems[x])
						CurrentMissionsTable.insert({"PlayerID":character.ObjectConfig["ObjectID"],
													 "MissionType":mission.MissionType,
													 "RewardCurrency":mission.RewardCurrency,
													 "RewardItems":rewardItems,
													 "RewardUniverseScore":mission.RewardUniverseScore,
													 "Offerer":mission.Offerer,
													 "Target":mission.Target,
													 "Progress":mission.Progress})

					inventory : Inventory = character.ObjectConfig["Inventory"]
					for item in inventory.InventoryList:
						InventoryTable.insert({"LOT":item["LOT"], "Slot":item["Slot"],
											   "Equipped":int(item["Equipped"]), "Linked":int(item["Linked"]),
											   "Quantity":item["Quantity"], "ObjectID":item["ObjectID"],
											   "OwnerID":character.ObjectConfig["ObjectID"]})

					posStr = "{},{},{}".format(character.ObjectConfig["Position"].X,character.ObjectConfig["Position"].Y,character.ObjectConfig["Position"].Z)
					rotStr = "{},{},{},{}".format(character.ObjectConfig["Rotation"].X,
											   character.ObjectConfig["Rotation"].Y,
											   character.ObjectConfig["Rotation"].Z,
												character.ObjectConfig["Rotation"].W)

					CharacterConfigTable.insert({"UniverseScore":character.ObjectConfig["UniverseScore"],
												 "Level":character.ObjectConfig["Level"],
												 "Health":character.ObjectConfig["Health"],
												 "MaxHealth":character.ObjectConfig["MaxHealth"],
												 "Armor":character.ObjectConfig["Armor"],
												 "MaxArmor": character.ObjectConfig["MaxArmor"],
												 "Imagination": character.ObjectConfig["Imagination"],
												 "MaxImagination": character.ObjectConfig["MaxImagination"],
												 "Currency": character.ObjectConfig["Currency"],
												 "PlayerID": character.ObjectConfig["ObjectID"],
												 "Position":posStr,
												 "Rotation":rotStr})

	def InitializeAccounts(self, Server : GameDB):
		self.Accounts = []
		AccountsTable : DBTable = Server.Tables["Accounts"]
		CharacterTable : DBTable = Server.Tables["Characters"]
		CharacterStats : DBTable = Server.Tables["CharacterStatistics"]
		CompMissionTable : DBTable = Server.Tables["CompletedMissions"]
		CurrentMissionsTable: DBTable = Server.Tables["CurrentMissions"]
		InventoryTable: DBTable = Server.Tables["Inventory"]
		CharacterConfigTable : DBTable = Server.Tables["CharacterConfig"]
		count = 0
		Accounts = AccountsTable.selectAll("AccountID != -1")
		for account in Accounts:
			AccountObject = Account(self)
			AccountObject.AccountID = int(account["AccountID"])
			AccountObject.Username = str(account["Username"])
			AccountObject.Password = str(account["Password"])
			AccountObject.Banned = bool(account["Banned"])
			AccountObject.IsAdmin = bool(account["IsAdmin"])
			Characters = CharacterTable.selectAll("AccountID = {}".format(account["AccountID"]))
			for character in Characters:
				PlayerStatistics = CharacterStats.selectAll("PlayerID = {}".format(character["ObjectID"]))[0]
				CompletedMissions = CompMissionTable.selectAll("PlayerID = {}".format(character["ObjectID"]))
				CurrentMissions = CurrentMissionsTable.selectAll("PlayerID = {}".format(character["ObjectID"]))
				PlayerInventory = InventoryTable.selectAll("OwnerID = {}".format(character["ObjectID"]))
				CharacterConfig = CharacterConfigTable.selectAll("PlayerID = {}".format(character["ObjectID"]))[0]

				LoadedPlayer : Character = Character(AccountObject)
				LoadedPlayer.ObjectConfig["ObjectID"] = character["ObjectID"]
				LoadedPlayer.Zone = character["Zone"]
				LoadedPlayer.ObjectConfig["Name"] = character["Name"]
				LoadedPlayer.ObjectConfig["ShirtColor"] = character["ShirtColor"]
				LoadedPlayer.ObjectConfig["ShirtStyle"] = character["ShirtStyle"]
				LoadedPlayer.ObjectConfig["PantsColor"] = character["PantsColor"]
				LoadedPlayer.ObjectConfig["HairColor"] = character["HairColor"]
				LoadedPlayer.ObjectConfig["HairStyle"] = character["HairStyle"]
				LoadedPlayer.ObjectConfig["lh"] = character["lh"]
				LoadedPlayer.ObjectConfig["rh"] = character["rh"]
				LoadedPlayer.ObjectConfig["Eyebrows"] = character["Eyebrows"]
				LoadedPlayer.ObjectConfig["Eyes"] = character["Eyes"]
				LoadedPlayer.ObjectConfig["Mouth"] = character["Mouth"]

				positionArray = str(CharacterConfig["Position"]).split(",")
				LoadedPlayer.ObjectConfig["Position"].set(float(positionArray[0]), float(positionArray[1]), float(positionArray[2]))
				rotationArray = str(CharacterConfig["Rotation"]).split(",")
				LoadedPlayer.ObjectConfig["Rotation"].set(float(rotationArray[0]), float(rotationArray[1]), float(rotationArray[2]), float(rotationArray[3]))
				LoadedPlayer.ObjectConfig["UniverseScore"] = CharacterConfig["UniverseScore"]
				LoadedPlayer.ObjectConfig["Level"] = CharacterConfig["Level"]
				LoadedPlayer.ObjectConfig["Health"] = CharacterConfig["Health"]
				LoadedPlayer.ObjectConfig["MaxHealth"] = CharacterConfig["MaxHealth"]
				LoadedPlayer.ObjectConfig["Armor"] = CharacterConfig["Armor"]
				LoadedPlayer.ObjectConfig["MaxArmor"] = CharacterConfig["MaxArmor"]
				LoadedPlayer.ObjectConfig["Imagination"] = CharacterConfig["Imagination"]
				LoadedPlayer.ObjectConfig["MaxImagination"] = CharacterConfig["MaxImagination"]
				LoadedPlayer.ObjectConfig["Currency"] = CharacterConfig["Currency"]

				for mission in CompletedMissions:
					LoadedPlayer.ObjectConfig["CompletedMissions"].append(int(mission["MissionID"]))

				for mission in CurrentMissions:
					MissionObject = Mission(LoadedPlayer)
					MissionObject.MissionType = mission["MissionType"]
					MissionObject.MissionID = mission["MissionID"]
					MissionObject.RewardCurrency = mission["RewardCurrency"]
					MissionObject.RewardItems = str(mission["RewardItems"]).split("|")
					MissionObject.RewardUniverseScore = mission["RewardUniverseScore"]
					MissionObject.Offerer = mission["Offerer"]
					MissionObject.Target = mission["Target"]
					MissionObject.Progress = mission["Progress"]
					LoadedPlayer.ObjectConfig["CurrentMissions"].append(MissionObject)

				for item in PlayerInventory:
					LoadedPlayer.ObjectConfig["Inventory"].addItem(LOT=int(item["LOT"]),
																   Slot=item["Slot"],
																   Equipped=bool(item["Equipped"]),
																   Linked=bool(item["Linked"]),
																   Quantity=int(item["Quantity"]),
																   ObjectID=item["ObjectID"])

				LoadedPlayer.ObjectConfig["CharacterStatistics"].CurrencyCollected = PlayerStatistics["CurrencyCollected"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].BricksCollected = PlayerStatistics["BricksCollected"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].SmashablesSmashed = PlayerStatistics["SmashablesSmashed"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].QuickBuildsDone = PlayerStatistics["QuickBuildsDone"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].EnemiesSmashed = PlayerStatistics["EnemiesSmashed"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].RocketsUsed = PlayerStatistics["RocketsUsed"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].PetsTamed = PlayerStatistics["PetsTamed"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].ImaginationCollected = PlayerStatistics["ImaginationCollected"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].HealthCollected = PlayerStatistics["HealthCollected"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].ArmorCollected = PlayerStatistics["ArmorCollected"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].DistanceTraveled = PlayerStatistics["DistanceTraveled"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].TimesDied = PlayerStatistics["TimesDied"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].DamageTaken = PlayerStatistics["DamageTaken"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].DamageHealed = PlayerStatistics["DamageHealed"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].ArmorRepaired = PlayerStatistics["ArmorRepaired"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].ImaginationRestored = PlayerStatistics["ImaginationRestored"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].ImaginationUsed = PlayerStatistics["ImaginationUsed"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].DistanceDriven = PlayerStatistics["DistanceDriven"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].TimeAirborneInCar = PlayerStatistics["TimeAirborneInCar"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].RacingImaginationCollected = PlayerStatistics["RacingImaginationCollected"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].RacingImaginationCratesSmashed = PlayerStatistics["RacingImaginationCratesSmashed"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].RaceCarBoosts = PlayerStatistics["RaceCarBoosts"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].CarWrecks = PlayerStatistics["CarWrecks"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].RacingSmashablesSmashed = PlayerStatistics["RacingSmashablesSmashed"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].RacesFinished = PlayerStatistics["RacesFinished"]
				LoadedPlayer.ObjectConfig["CharacterStatistics"].RacesWon = PlayerStatistics["RacesWon"]

				AccountObject.Characters.append(LoadedPlayer)
				print("Initialized Character {}".format(character["ObjectID"]))
			self.Accounts.append(AccountObject)
			count += 1
		print("Initialized {} Account(s)".format(count))


class Account():
	def __init__(self, Parent):
		self.Parent = Parent
		self.Username: str = None
		self.Password: str = None
		self.Banned: bool = False
		self.IsAdmin : bool = False
		self.Characters: list = []
		self.AccountID : int = 0

	def CreateMinifigure(self, Name: str, ShirtColor: int, ShirtStyle: int, PantsColor: int, HairColor: int,
						 HairStyle: int, lh: int, rh: int, Eyebrows: int, Eyes: int, Mouth: int):
		Minifigure = Character(self)
		Minifigure.Zone = 1000
		Minifigure.ObjectConfig["Name"] = Name
		Minifigure.ObjectConfig["ShirtColor"] = ShirtColor
		Minifigure.ObjectConfig["ShirtStyle"] = ShirtStyle
		Minifigure.ObjectConfig["PantsColor"] = PantsColor
		Minifigure.ObjectConfig["HairColor"] = HairColor
		Minifigure.ObjectConfig["HairStyle"] = HairStyle
		Minifigure.ObjectConfig["lh"] = lh
		Minifigure.ObjectConfig["rh"] = rh
		Minifigure.ObjectConfig["ObjectID"] = random.randint(100000000000000000, 999999999999999999)
		Minifigure.ObjectConfig["Eyebrows"] = Eyebrows
		Minifigure.ObjectConfig["Eyes"] = Eyes
		Minifigure.ObjectConfig["Mouth"] = Mouth
		shirtLOT = getShirtID(ShirtColor, ShirtStyle)
		pantsLOT = getPantsID(PantsColor)
		Minifigure.ObjectConfig["Inventory"].addItem(shirtLOT, random.randint(100000000000000000, 999999999999999999), Equipped=True)
		Minifigure.ObjectConfig["Inventory"].addItem(pantsLOT, random.randint(100000000000000000, 999999999999999999), Equipped=True)
		self.Characters.append(Minifigure)
from enum import *

class ClothingLOT(IntEnum):
	#Shirts
	SHIRT_BRIGHT_RED = 4049
	SHIRT_BRIGHT_BLUE = 4083
	SHIRT_BRIGHT_YELLOW = 4117
	SHIRT_DARK_GREEN = 4151
	SHIRT_BRIGHT_ORANGE = 4185
	SHIRT_BLACK = 4219
	SHIRT_DARK_STONE_GRAY = 4253
	SHIRT_MEDIUM_STONE_GRAY = 4287
	SHIRT_REDDISH_BROWN = 4321
	SHIRT_WHITE = 4355
	SHIRT_MEDIUM_BLUE = 4389
	SHIRT_DARK_RED = 4423
	SHIRT_EARTH_BLUE = 4457
	SHIRT_EARTH_GREEN = 4491
	SHIRT_BRICK_YELLOW = 4525
	SHIRT_SAND_BLUE = 4559
	SHIRT_SAND_GREEN = 4593
	#Pants
	PANTS_BRIGHT_RED = 2508
	PANTS_BRIGHT_ORANGE = 2509
	PANTS_BRICK_YELLOW = 2511
	PANTS_MEDIUM_BLUE = 2513
	PANTS_SAND_GREEN = 2514
	PANTS_DARK_GREEN = 2515
	PANTS_EARTH_GREEN = 2516
	PANTS_EARTH_BLUE = 2517
	PANTS_BRIGHT_BLUE = 2519
	PANTS_SAND_BLUE = 2520
	PANTS_DARK_STONE_GRAY = 2521
	PANTS_MEDIUM_STONE_GRAY = 2522
	PANTS_WHITE = 2523
	PANTS_BLACK = 2524
	PANTS_REDDISH_BROWN = 2526
	PANTS_DARK_RED = 2527

class DisconnectionReasons(IntEnum):
	UnknownError = 0x00
	DuplicateLogin = 0x04
	ServerShutdown = 0x05
	ServerCannotLoadMap = 0x06
	InvalidSessionKey = 0x07
	CharacterNotFound = 0x09
	CharacterCorruption = 0x0a
	Kicked = 0x0b

class LoginResponseEnum(IntEnum):
	Success = 0x01
	Banned = 0x02
	InvalidPerm = 0x03
	InvalidLoginInfo = 0x06
	AccountLocked = 0x07


class ZoneID(IntEnum):
	NoZone = 0
	VentureExplorer = 1000
	ReturnToVentureExplorer = 1001
	AvantGardens = 1100
	AvantGardensSurvival = 1101
	SpiderQueenBattle = 1102
	BlockYard = 1150
	AvantGrove = 1151
	NimbusStation = 1200
	PetCove = 1201
	VertigoLoop = 1203
	BattleOfNimbusStation = 1204
	NimbusRock = 1250
	NimbusIsle = 1251
	GnarledForest = 1300
	CanyonCove = 1302
	KeelhaulCanyon = 1303
	ChanteyShantey = 1350
	ForbiddenValley = 1400
	ForbiddenValleyDragon = 1402
	DragonmawChasm = 1403
	RavenBluff = 1450
	Starbase3001 = 1600
	DeepFreeze = 1601
	RobotCity = 1602
	MoonBase = 1603
	Portabello = 1604
	LEGOClub = 1700
	CruxPrime = 1800
	NexusTower = 1900
	Ninjago = 2000
	FrakjawBattle = 2001

class SessionState(IntEnum):
	LoggingIn = 0
	CharacterScreen = 1
	InGame = 3

class MinifigureCreationResponse(IntEnum):
	Success = 0x00
	IDNotWorking = 0x01
	NameNotAllowed = 0x02
	PredefinedNameInUse = 0x03
	NameInUse = 0x04

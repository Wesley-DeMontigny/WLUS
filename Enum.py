from enum import *
from structures import Vector3
from os import listdir


class ClothingLOT(IntEnum):
	# Shirts
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
	# Pants
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

class ReplicaTypes(IntEnum):
	Construction = 0
	Serialization = 1

ZoneChecksums = {
    1000: 0x20b8087c,
    1001: 0x26680a3c,
    1100: 0x49525511,
    1101: 0x538214e2,
    1102: 0x0fd403da,
    1150: 0x0fd403da,
    1151: 0x0a890303,
    1200: 0xda1e6b30,
    1201: 0x476e1330,
    1203: 0x10fc0502,
    1204: 0x07d40258,
	1250: 0x058d0191,
	1251: 0x094f045d,
	1300: 0x12eac290,
	1302: 0x0b7702ef,
	1303: 0x152e078a,
	1350: 0x04b6015c,
	1400: 0x8519760d,
	1402: 0x02f50187,
	1403: 0x81850f4e,
	1450: 0x03f00126,
	1600: 0x07c202ee,
	1601: 0x02320106,
	1602: 0x0793037f,
	1603: 0x043b01ad,
	1604: 0x181507dd,
	1700: 0x02040138,
	1800: 0x4b17a399,
	1900: 0x9e4af43c,
	2000: 0x4d692c74,
	2001: 0x09eb00ef
}

nimbus_lvl = []
for file in listdir("resources/nimbus_station_lvl"):
	nimbus_lvl.append("resources/nimbus_station_lvl/"+file)
avant_lvl = []
for file in listdir("resources/avant_gardens_lvl"):
	avant_lvl.append("resources/avant_gardens_lvl/"+file)
fv_lvl = []
for file in listdir("resources/forbidden_valley_lvl"):
	fv_lvl.append("resources/forbidden_valley_lvl/"+file)
gnarled_lvl = []
for file in listdir("resources/gnarled_forest_lvl"):
	gnarled_lvl.append("resources/gnarled_forest_lvl/"+file)
ninjago_lvl = []
for file in listdir("resources/ninjago_lvl"):
	ninjago_lvl.append("resources/ninjago_lvl/"+file)
nexus_lvl = []
for file in listdir("resources/nexus_tower_lvl"):
	nexus_lvl.append("resources/nexus_tower_lvl/"+file)
ZoneLvls = {1000 : ["resources/nd_space_ship.lvl"],
			1001: [],
			1100: avant_lvl,
			1101: [],
			1102: [],
			1150: [],
			1151: [],
			1200: nimbus_lvl,
			1201: ["resources/nd_ns_pet_ranch.lvl"],
			1203: [],
			1204: [],
			1250: [],
			1251: [],
			1300: gnarled_lvl,
			1302: [],
			1303: [],
			1350: [],
			1400: fv_lvl,
			1402: [],
			1403: [],
			1450: [],
			1600: ["resources/nd_starbase3001.lvl"],
			1601: ["resources/wbl_deep_freeze_intro.lvl"],
			1602: ["resources/wbl_robot_city_intro.lvl"],
			1603: ["resources/wbl_moon_base_intro.lvl"],
			1604: ["resources/wbl_portabello.lvl"],
			1700: ["resources/nd_lego_club.lvl"],
			1800: [],
			1900: nexus_lvl,
			2000: ninjago_lvl,
			2001: []
			}

DefaultZoneSpawns = {1000 : Vector3(-624.13, 613.326233, -30.974),
		1001 : Vector3(-187.2391, 608.2743, 54.5554352),
		1100 : Vector3(522.9949, 406.040375, 129.992722),
		1101 : Vector3(35.0297, 365.780426, -201.578369),
		1102 : Vector3(-18.7062054, 440.20932, 37.5326424),
		1150 : Vector3(-18.7062054, 440.20932, 37.5326424),
		1151 : Vector3(25.0526543, 472.215027, -24.318882),
		1200 : Vector3(-40.0, 293.047, -16.0),
		1201 : Vector3(111.670906, 229.282776, 179.87793),
		1203 : Vector3(0.0, 0.0, 0.0),
		1204 : Vector3(-12.1019106, 212.900024, 191.147964),
		1250 : Vector3(-17.8299046, 440.509674, 30.0326862),
		1251 : Vector3(31.55009, 470.885254, 193.457321),
		1300 : Vector3(-329.965881, 302.470184, -470.232758),
		1302 : Vector3(-293.072571, 233.0, -4.16148),
		1303 : Vector3(0.0, 0.0, 0.0),
		1350 : Vector3(-19.713892, 440.20932, 26.935009),
		1400 : Vector3(390.284363, 229.452881, -511.350983),
		1402 : Vector3(-264.426575, 290.3452, 308.619049),
		1403 : Vector3(-1457.71826, 794.0, -332.2917),
		1450 : Vector3(-26.8431015, 425.11496, 53.7349777),
		1600 : Vector3(34.6352119, 1571.29309, 48.0321465),
		1601 : Vector3(-90.30964, 211.087067, -126.3196),
		1602 : Vector3(-163.2, 217.254913, 172.0),
		1603 : Vector3(9.18036652, 48.79997, 109.610374),
		1604 : Vector3(-99.80103, 231.916946, -162.67955),
		1700 : Vector3(-359.979156, 1066.328, -369.287781),
		1800 : Vector3(-241.965515, 92.78052, 557.327942),
		1900 : Vector3(165.355682, 1164.17822, -543.9093),
		2000 : Vector3(-446.79715, 171.158859, 1122.83545),
		2001 : Vector3(11.26009, 211.05188, 40.6721039)}

ZoneNames = {1000 : "Venture Explorer",
			 1001 : "Return To The Venture Explorer",
			 1100 : "Avant Gardens",
			 1101 : "Avant Gardens Survival",
			 1102 : "Spider Queen Battle",
			 1150 : "Block Yard",
			 1151 : "Avant Grove",
			 1200 : "Nimbus Station",
			 1201 : "Pet Cove",
			 1203 : "Vertigo Loop",
			 1204 : "Battle of Nimbus Station",
			 1250 : "Nimbus Rock",
			 1251 : "Nimbus Isle",
			 1300 : "Gnarled Forest",
			 1302 : "Canyon Cove",
			 1303 : "Keelhaul Canyon",
			 1350 : "Chantey Shantey",
			 1400 : "Forbidden Valley",
			 1402 : "Forbidden Valley Dragon",
			 1403 : "Dragonmaw Chasm",
			 1450 : "Raven Bluff",
			 1600 : "Starbase 3001",
			 1601 : "Deep Freeze",
			 1602 : "Robot City",
			 1603 : "Moon Base",
			 1604 : "Portabello",
			 1700 : "LEGO Club",
			 1800 : "Crux Prime",
			 1900 : "Nexus Tower",
			 2000 : "Ninjago Monastery",
			 2001 : "Frakjaw Battle"}

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

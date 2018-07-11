import sys
sys.path.append("..")
import scripts
import game_types



zone_checksums = {1000: 0x20b8087c,
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
	2001: 0x09eb00ef}
zone_spawns = {1000: game_types.Vector3(-624.13, 613.326233, -30.974),
					1001: game_types.Vector3(-187.2391, 608.2743, 54.5554352),
					1100: game_types.Vector3(522.9949, 406.040375, 129.992722),
					1101: game_types.Vector3(35.0297, 365.780426, -201.578369),
					1102: game_types.Vector3(-18.7062054, 440.20932, 37.5326424),
					1150: game_types.Vector3(-18.7062054, 440.20932, 37.5326424),
					1151: game_types.Vector3(25.0526543, 472.215027, -24.318882),
					1200: game_types.Vector3(-40.0, 293.047, -16.0),
					1201: game_types.Vector3(111.670906, 229.282776, 179.87793),
					1203: game_types.Vector3(0.0, 0.0, 0.0),
					1204: game_types.Vector3(-12.1019106, 212.900024, 191.147964),
					1250: game_types.Vector3(-17.8299046, 440.509674, 30.0326862),
					1251: game_types.Vector3(31.55009, 470.885254, 193.457321),
					1300: game_types.Vector3(-329.965881, 302.470184, -470.232758),
					1302: game_types.Vector3(-293.072571, 233.0, -4.16148),
					1303: game_types.Vector3(0.0, 0.0, 0.0),
					1350: game_types.Vector3(-19.713892, 440.20932, 26.935009),
					1400: game_types.Vector3(390.284363, 229.452881, -511.350983),
					1402: game_types.Vector3(-264.426575, 290.3452, 308.619049),
					1403: game_types.Vector3(-1457.71826, 794.0, -332.2917),
					1450: game_types.Vector3(-26.8431015, 425.11496, 53.7349777),
					1600: game_types.Vector3(34.6352119, 1571.29309, 48.0321465),
					1601: game_types.Vector3(-90.30964, 211.087067, -126.3196),
					1602: game_types.Vector3(-163.2, 217.254913, 172.0),
					1603: game_types.Vector3(9.18036652, 48.79997, 109.610374),
					1604: game_types.Vector3(-99.80103, 231.916946, -162.67955),
					1700: game_types.Vector3(-359.979156, 1066.328, -369.287781),
					1800: game_types.Vector3(-241.965515, 92.78052, 557.327942),
					1900: game_types.Vector3(165.355682, 1164.17822, -543.9093),
					2000: game_types.Vector3(-446.79715, 171.158859, 1122.83545),
					2001: game_types.Vector3(11.26009, 211.05188, 40.6721039)}
zone_names = {1000: "Venture Explorer",
				   1001: "Return To The Venture Explorer",
				   1100: "Avant Gardens",
				   1101: "Avant Gardens Survival",
				   1102: "Spider Queen Battle",
				   1150: "Block Yard",
				   1151: "Avant Grove",
				   1200: "Nimbus Station",
				   1201: "Pet Cove",
				   1203: "Vertigo Loop",
				   1204: "Battle of Nimbus Station",
				   1250: "Nimbus Rock",
				   1251: "Nimbus Isle",
				   1300: "Gnarled Forest",
				   1302: "Canyon Cove",
				   1303: "Keelhaul Canyon",
				   1350: "Chantey Shantey",
				   1400: "Forbidden Valley",
				   1402: "Forbidden Valley Dragon",
				   1403: "Dragonmaw Chasm",
				   1450: "Raven Bluff",
				   1600: "Starbase 3001",
				   1601: "Deep Freeze",
				   1602: "Robot City",
				   1603: "Moon Base",
				   1604: "Portabello",
				   1700: "LEGO Club",
				   1800: "Crux Prime",
				   1900: "Nexus Tower",
				   2000: "Ninjago Monastery",
				   2001: "Frakjaw Battle"}

class Main(scripts.Script):
	def __init__(self, parent):
		super().__init__(parent, "on_boot")
		global game

		game = self.get_parent()

	def run(self):
		@game.register_event_handler("ServiceRegistered")
		def register_zones(service):
			if (service.get_name() == "World"):
				for zone in zone_names:
					service.register_zone(zone_id=zone, load_id=zone, checksum=zone_checksums[zone], spawn_loc=zone_spawns[zone], name=zone_names[zone])
					print("Registered {}!".format(zone_names[zone]))



import sys
sys.path.append("..")
import scripts
import game_types
from pyraknet.bitstream import ReadStream


zone_checksums = {1000: 0x20b8087c,
	1001: 0x26680a3c,
	1100: 0x49525511,
	#1101: 0x538214e2,
	1102: 0x0fd403da,
	1150: 0x0fd403da,
	1151: 0x0a890303,
	1200: 0xda1e6b30,
	1201: 0x476e1330,
	#1203: 0x10fc0502,
	1204: 0x07d40258,
	1250: 0x058d0191,
	1251: 0x094f045d,
	1300: 0x12eac290,
	1302: 0x0b7702ef,
	#1303: 0x152e078a,
	1350: 0x04b6015c,
	1400: 0x8519760d,
	1402: 0x02f50187,
	#1403: 0x81850f4e,
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

class Main(scripts.Script):
	def __init__(self, parent):
		super().__init__(parent, "on_boot")
		global game
		game = self.get_parent()

	def run(self):
		@game.register_event_handler("GameStarted", threaded=True)
		def register_zones():
			world_service = game.get_service("World")
			cdclient = game.get_service("Database").cdclient_db
			c = cdclient.connection.cursor()
			for zone in zone_checksums:
				json = {}
				spawn_rot = game_types.Vector4()
				c.execute("SELECT * FROM ZoneTable WHERE zoneID = ?", (zone,))
				zone_data = c.fetchone()
				luz_path = f"resources/{zone_data['zoneName']}"
				name = zone_data["DisplayDescription"]
				luz_file = open(luz_path, "rb")
				stream = ReadStream(luz_file.read())
				luz = game_types.LUZ().deserialize(stream)
				luz_file.close()
				spawn_loc = luz.config["spawnpoint_pos"]
				spawn_rot = luz.config["spawnpoint_rot"]
				folder = ""
				path_folders = luz_path.split("/")
				path_folders = path_folders[:-1]
				for path_folder in path_folders:
					folder += path_folder + "/"
				json["zone_path"] = folder
				json["scenes"] = luz.config["scenes"]
				world_service.register_zone(zone_id=zone, load_id=zone, checksum=zone_checksums[zone], spawn_loc=spawn_loc, spawn_rot=spawn_rot, name=name, json = json)
				print(f"Registered {name}!")
			game.trigger_event("BootUp_WorldsRegistered")



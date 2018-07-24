import sys
sys.path.append("..")
import scripts
import json
import game_types



class Main(scripts.Script):
	def __init__(self, parent):
		super().__init__(parent, "load_objects")
		global game
		game = self.get_parent()

	def run(self):
		@game.register_event_handler("BootUp_WorldsRegistered", threaded=True)
		def load_objects():
			world_service = game.get_service("World")
			database_service = game.get_service("Database")
			server_db = database_service.server_db
			objects = server_db.tables["ZoneObjects"].select_all("zone_id != -1")
			for object in objects:
				zone = world_service.get_zone_by_id(object["zone_id"])
				if(zone is not None):
					adjusted_config = json.loads(object["replica_config"])
					if("position" in adjusted_config):
						adjusted_config["position"] = game_types.Vector3(str_val=adjusted_config["position"])
					if("rotation" in adjusted_config):
						adjusted_config["rotation"] = game_types.Vector4(str_val=adjusted_config["rotation"])
					zone.create_object(zone, adjusted_config)
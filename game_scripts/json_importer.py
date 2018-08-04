import sys
sys.path.append("..")
import scripts
import os
import json
import game_types
import random

class Main(scripts.Script):
	def __init__(self, parent):
		super().__init__(parent, "JSON Importer")
		global game
		game = self.get_parent()

	def run(self):
		game.register_console_command("ImportLUZ", self.import_handler)

	def import_handler(self, args):
		if(len(args) == 1):
			zone = int(args[0])

			file_path = input("JSON Directory: ")
			if(file_path == ''):
				return

			lvl_files = []

			luz = open(file_path, "r")
			luz_json = json.loads(luz.read())
			folder = '\\'.join(file_path.split('\\')[0:-1])
			for scene in luz_json["scenes"]:
				lvl_files.append({"scene_id":scene["id"], "path":folder+"/"+scene["filename"]+".json"})

			for lvl in lvl_files:
				file = open(lvl["path"], "r")
				json_obj = json.loads(file.read())

				database = game.get_service("Database")
				server_db = database.server_db
				zone_objects = server_db.tables["ZoneObjects"]

				for chunk in json_obj["chunks"]:
					if(chunk["_type"] == 2001):
						object_id = random.randint(100000000000000000, 999999999999900000)
						for game_object in chunk["objects"]:
							if("spawntemplate" in game_object["settings"] and ("renderDisabled" not in game_object["settings"] or game_object["settings"]["renderDisabled"] == False)):
								object_id += 1
								config = {'lot':game_object["settings"]["spawntemplate"], 'spawner_id':game_object["id"],
										  'position': str(game_types.Vector3(game_object['pos']['pos']['x'], game_object['pos']['pos']['y'], game_object['pos']['pos']['z'])),
										  'rotation': str(game_types.Vector4(game_object['pos']['rot']['x'], game_object['pos']['rot']['y'], game_object['pos']['rot']['z'], game_object['pos']['rot']['w'])),
										  'scale':game_object["scale"], 'spawner_node_id':0, 'object_id':object_id, 'scene':lvl["scene_id"]}
								zone_objects.insert({"zone_id": zone, "replica_config": json.dumps(config)})
								print("Imported Object {} To DB".format(config["object_id"]))



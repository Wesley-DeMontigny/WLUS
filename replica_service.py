import services
import game_objects
import game_types
import components
import game_enums
import re
from pyraknet.bitstream import *

class ReplicaService(services.GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Replica"
		global game
		game = self.get_parent()

	def create_replica_object(self, parent, zone, config : dict):
		if("lot" not in config):
			raise Exception("'create_replica_object' Requires A LOT In The Conifg!")
		replica = game_objects.ReplicaObject(parent, zone, config)

		transform : components.Transform = replica.get_component(components.Transform)
		if("position" in config):
			transform.position = config["position"]
		if("rotation" in config):
			transform.rotation = config["rotation"]
		if("scale" in config):
			transform.scale = config["scale"]

		cdclient_db = game.get_service("Database").cdclient_db
		component_list = cdclient_db.tables["ComponentsRegistry"].select(["component_type", "component_id"], "id = {}".format(config["lot"]))
		object_components = {}
		for component in component_list:
			object_components[int(component["component_type"])] = int(component["component_id"])

		if(108 in object_components):
			possesable = components.Possessable(replica)
			if("driver_object_id" in config):
				possesable.driver_object_id = config["driver_object_id"]
			replica.add_component(possesable)
		if(61 in object_components):
			module_assembly = components.ModuleAssembly(replica)
			replica.add_component(module_assembly)
		if(30 in object_components):
			vehicle_physics = components.VehiclePhysics(replica)
			replica.add_component(vehicle_physics)
		if(7 in object_components):
			destructible = components.Destructible(replica)
			replica.add_component(destructible)

			destructible_data = cdclient_db.tables["DestructibleComponent"].select_all("id = {}".format(object_components[7]))[0]
			stats = components.Stats(replica)
			stats.health = destructible_data["life"]
			stats.max_health = destructible_data["life"]
			stats.armor = destructible_data["armor"]
			stats.max_armor = destructible_data["armor"]
			stats.imagination = destructible_data["imagination"]
			stats.max_imagination = destructible_data["imagination"]
			stats.faction = destructible_data["faction"]
			stats.is_smashable = destructible_data["isSmashable"]

			if("health" in config):
				stats.health = config["health"]
			if("max_health" in config):
				stats.max_health = config["max_health"]
			if("armor" in config):
				stats.armor = config["armor"]
			if("max_armor" in config):
				stats.max_armor = config["max_armor"]
			if("imagination" in config):
				stats.imagination = config["imagination"]
			if("max_imagination" in config):
				stats.max_imagination = config["max_imagination"]
			if("faction" in config):
				stats.faction = config["faction"]
			if("is_smashable" in config):
				stats.is_smashable = config["is_smashable"]
			replica.add_component(stats)
		if(23 in object_components):
			if(replica.get_component(components.Stats) is None):
				stats = components.Stats(replica)
				replica.add_component(stats)

			collectible = components.Collectible(replica)
			if("collectible_id" in config):
				collectible.collectible_id = config["collectible_id"]
			replica.add_component(collectible)
		if(26 in object_components):
			#TODO: Actually Implement The Config
			pet = components.Pet(replica)
			replica.add_component(pet)
		if(4 in object_components):
			character = components.Character(replica, replica.get_object_id())
			replica.add_component(character)
		if(17 in object_components):
			inventory = components.Inventory(replica)
			if(game.get_service("Player").get_player_by_id(replica.get_object_id()) is not None):
				inventory.items = game.get_service("Player").get_player_by_id(replica.get_object_id())["Inventory"]
			db_items = cdclient_db.tables["InventoryComponent"].select_all("id = {}".format(object_components[17]))
			for item in db_items:
				new_item = {}
				new_item["item_id"] = game.generate_object_id()
				new_item["lot"] = item["itemid"]
				new_item["quantity"] = item["count"]
				new_item["equipped"] = item["equip"]
				new_item["linked"] = 0
				new_item["slot"] = 0
				new_item["json"] = {"from_db":1}
				inventory.add_item(new_item)
			replica.add_component(inventory)
		if(5 in object_components):
			script_comp = components.ScriptComponent(replica)
			replica.add_component(script_comp)
		if(9 in object_components):
			skill = components.Skill(replica)
			replica.add_component(skill)
		if(60 in object_components):
			base_comabt_ai = components.BaseCombatAI(replica)
			replica.add_component(base_comabt_ai)
		if(48 in object_components):
			rebuild = components.Rebuild(replica)
			db_rebuild = cdclient_db.tables["RebuildComponent"].select_all("id = {}".format(object_components[48]))[0]
			rebuild.reset_time = float(db_rebuild["reset_time"])
			if("build_activator_pos" in config):
				rebuild.build_activator_pos = config["build_activator_pos"]
			if("build_enabled" in config):
				rebuild.enabled = config["build_enabled"]
			replica.add_component(rebuild)

			if(replica.get_component(components.Stats) is None):
				stats = components.Stats(replica)
				stats.imagination = int(db_rebuild["take_imagination"])
				stats.max_imagination = int(db_rebuild["take_imagination"])
				replica.add_component(stats)
		if(25 in object_components):
			moving_platform = components.MovingPlatform(replica)
			replica.add_component(moving_platform)
		if(49 in object_components):
			switch = components.Switch(replica)
			replica.add_component(switch)
		if(16 in object_components):
			vendor = components.Vendor(replica)
			replica.add_component(vendor)
		if(6 in object_components):
			bouncer = components.Bouncer(replica)
			replica.add_component(bouncer)
		if(39 in object_components):
			scripted_activity = components.ScriptedActivity(replica)
			replica.add_component(scripted_activity)
		if(71 in object_components):
			racing_control = components.RacingControl(replica)
			replica.add_component(racing_control)
		if(75 in object_components):
			exhibit = components.LUPExhibit(replica)
			replica.add_component(exhibit)
		if(2 in object_components):
			render = components.Render(replica)
			replica.add_component(render)
		if(107 in object_components):
			comp107 = components.Component107(replica)
			replica.add_component(comp107)
		if(69 in object_components):
			trigger = components.Trigger(replica)
			replica.add_component(trigger)

		return replica


	def parse_struct(self, file_path):
		write_methods = {"bit":"c_bit", "float":"c_float", "double":"c_double", "s8":"c_int8", "u8":"c_uint8", "s16":"c_int16", "u16":"c_uint16", "s32":"c_int32", "u32":"c_uint32", "s64":"c_int64", "u64":"c_uint64",
						 "lot":"c_long"}
		execute_string = ""
		indent_level = 0
		def format_line(string, indentation_level):
			indent_string = ""
			for i in range(indentation_level):
				indent_string += "    "
			return indent_string + string + "\n"
		with open(file_path, "r") as file:
			for line in file:
				line = line.split("#")[0]#Filter out comments
				line = line.strip()
				if(line[:1] == "["):#Line is trying to write something to the stream
					data_type = line[line.find("[")+1:line.find("]")]
					write_value = line[line.find("{")+1:line.find("}")]
					write_str = ""
					if(data_type in write_methods):
						write_str = "stream.write({}({}))".format(write_methods[data_type], write_value)
					else:
						if(len(data_type.split("-")) == 2 and data_type.split("-")[1] == "string"):#If it says string at the start then write it via the String data type in game_types
							write_str = "stream.write(game_types.String({}, length_type={}))".format(write_value, write_methods[data_type.split("-")[0]])
						elif(len(data_type.split("-")) == 2 and data_type.split("-")[1] == "wstring"):
							write_str = "stream.write({}, length_type={})".format(write_value, write_methods[data_type.split("-")[0]])
						elif(data_type == "ldf"):
							write_str = "stream.write({})".format(write_value)
					execute_string += format_line(write_str, indent_level)
					execute_string += format_line("previous = {}".format(write_value), indent_level)
				elif(line[:2] == "{%"):#Line is setting a condition or ending one
					conditional = line[line.find("{%")+2:line.find("%}")]
					if(conditional == "end"):
						indent_level -= 1
					else:
						execute_string += format_line(conditional+":", indent_level)
						indent_level += 1
				elif(line[:1] == "{"):
					write_value = line[line.find("{")+1:line.find("}")]
					execute_string += format_line(write_value, indent_level)
		return execute_string

	def write_to_stream(self, replica : game_objects.ReplicaObject, stream : WriteStream, replica_type):
		exec(self.parse_struct("replica/creation_header.structs"))
		exec(self.parse_struct("replica/serialization_header.structs"))

		cdclient_db = game.get_service("Database").cdclient_db
		component_list = cdclient_db.tables["ComponentsRegistry"].select(["component_type", "component_id"], "id = {}".format(replica.lot))
		object_components = []
		for component in component_list:
			object_components.append(int(component["component_type"]))


		if(108 in object_components):
			exec(self.parse_struct("replica/components/Component 108.structs"))
		if(61 in object_components):
			exec(self.parse_struct("replica/components/ModuleAssembly.structs"))
		if(1 in object_components):
			exec(self.parse_struct("replica/components/ControllablePhysics.structs"))
		if(3 in object_components):
			exec(self.parse_struct("replica/components/SimplePhysics.structs"))
		if(20 in object_components):
			exec(self.parse_struct("replica/components/RigidBodyPhantomPhysics.structs"))
		if(30 in object_components):
			exec(self.parse_struct("replica/components/VehiclePhysics.structs"))
		if(40 in object_components):
			exec(self.parse_struct("replica/components/PhantomPhysics.structs"))
		if(7 in object_components):
			exec(self.parse_struct("replica/components/Destructible.structs"))
			exec(self.parse_struct("replica/components/Stats.structs"))
		if(23 in object_components):
			exec(self.parse_struct("replica/components/Stats.structs"))
			exec(self.parse_struct("replica/components/Collectible.structs"))
		if(26 in object_components):
			exec(self.parse_struct("replica/components/Pet.structs"))
		if(4 in object_components):
			exec(self.parse_struct("replica/components/Character.structs"))
		if(19 in object_components):
			exec(self.parse_struct("replica/components/Shooting Gallery.structs"))
		if(17 in object_components):
			exec(self.parse_struct("replica/components/Inventory.structs"))
		if(5 in object_components):
			exec(self.parse_struct("replica/components/Script.structs"))
		if(9 in object_components):
			exec(self.parse_struct("replica/components/Skill.structs"))
		if(60 in object_components):
			exec(self.parse_struct("replica/components/BaseCombatAI.structs"))
		if(48 in object_components):
			exec(self.parse_struct("replica/components/Stats.structs"))
			exec(self.parse_struct("replica/components/Rebuild.structs"))
		if(25 in object_components):
			exec(self.parse_struct("replica/components/MovingPlatform.structs"))
		if(49 in object_components):
			exec(self.parse_struct("replica/components/Switch.structs"))
		if(16 in object_components):
			exec(self.parse_struct("replica/components/Vendor.structs"))
		if(6 in object_components):
			exec(self.parse_struct("replica/components/Bouncer.structs"))
		if(39 in object_components):
			exec(self.parse_struct("replica/components/ScriptedActivity.structs"))
		if(71 in object_components):
			exec(self.parse_struct("replica/components/RacingControl.structs"))
		if(75 in object_components):
			exec(self.parse_struct("replica/components/Exhibit.structs"))
		if(42 in object_components):
			exec(self.parse_struct("replica/components/Model.structs"))
		if(2 in object_components):
			exec(self.parse_struct("replica/components/Render.structs"))
		if(50 in object_components):
			pass#Minigame?
		if(107 in object_components):
			exec(self.parse_struct("replica/components/Component 107.structs"))
		if(69 in object_components):
			exec(self.parse_struct("replica/components/Trigger.structs"))
















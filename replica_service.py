import services
import game_objects
import game_types
import components
import game_enums
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

		transform : components.Transform = replica.get_component("Transform")
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
				inventory.items.append(new_item)
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




	def write_to_stream(self, replica : game_objects.ReplicaObject, stream : WriteStream, type):
		#TODO: Add Component Whitelist
		#Base Data
		if(type == game_enums.ReplicaTypes.CONSTRUCTION):
			stream.write(c_longlong(replica.get_object_id()))
			stream.write(c_long(replica.lot))
			stream.write(replica.get_name(), length_type=c_ubyte)
			stream.write(c_ulong(0))
			if(replica.get_component(components.ModelData) is not None):
				stream.write(c_bit(True))
				replica.get_component(components.ModelData).ldf.write_to_stream(stream)
			else:
				stream.write(c_bit(False))
			stream.write(c_bit(replica.get_component(components.Trigger) is not None))
			if(replica.spawner_id is not None):
				stream.write(c_bit(True))
				stream.write(c_longlong(replica.spawner_id))
			else:
				stream.write(c_bit(False))
			if(replica.spawner_node_id is not None):
				stream.write(c_bit(True))
				stream.write(c_ulong(replica.spawner_node_id))
			else:
				stream.write(c_bit(False))
			stream.write(c_bit(True))
			stream.write(c_float(replica.get_component(components.Transform).scale))
			if(replica.world_state is not None):
				stream.write(c_bit(True))
				stream.write(c_ubyte(replica.world_state))
			else:
				stream.write(c_bit(False))
			if(replica.gm_level is not None):
				stream.write(c_bit(True))
				stream.write(c_ubyte(replica.gm_level))
			else:
				stream.write(c_bit(False))

		#Children/Parent Info
		if(self.get_children() != [] or isinstance(self.get_parent(), game_objects.ReplicaObject)):
			stream.write(c_bit(True))
			if(isinstance(self.get_parent(), game_objects.ReplicaObject)):
				stream.write(c_bit(True))
				stream.write(c_longlong(self.get_parent().get_object_id()))
				stream.write(c_bit(False))
			else:
				stream.write(c_bit(False))
			if(self.get_children() != []):
				stream.write(c_bit(True))
				stream.write(c_ushort(len(replica.get_children())))
				for child in self.get_children():
					stream.write(c_longlong(child.get_object_id()))
			else:
				stream.write(c_bit(False))
		else:
			stream.write(c_bit(False))


		cdclient_db = game.get_service("Database").cdclient_db
		component_list = cdclient_db.tables["ComponentsRegistry"].select(["component_type", "component_id"], "id = {}".format(replica.lot))
		object_components = []
		for component in component_list:
			object_components.append(int(component["component_type"]))


		if(108 in object_components):
			possesable = replica.get_component(components.Possessable)
			if(possesable.driver_object_id is not None and possesable.driver_object_id != 0):
				stream.write(c_bit(True))
				stream.write(c_bit(True))
				stream.write(c_longlong(possesable.driver_object_id))
				stream.write(c_bit(False))
				stream.write(c_bit(False))
			else:
				stream.write(c_bit(False))
		if(61 in object_components):
			module_assembly = replica.get_component(components.ModuleAssembly)
			#TODO: Figure out what this is and implement it
			stream.write(c_bit(module_assembly.flag_1))
		if(1 in object_components):
			transform = replica.get_component(components.Transform)
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_bit(False))
				stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_bit(True))
			stream.write(c_float(transform.position.X))
			stream.write(c_float(transform.position.Y))
			stream.write(c_float(transform.position.Z))
			stream.write(c_float(transform.rotation.X))
			stream.write(c_float(transform.rotation.Y))
			stream.write(c_float(transform.rotation.Z))
			stream.write(c_float(transform.rotation.W))
			stream.write(c_bit(transform.on_ground))
			stream.write(c_bit(False))
			stream.write(c_bit(True))
			stream.write(c_float(transform.velocity.X))
			stream.write(c_float(transform.velocity.Y))
			stream.write(c_float(transform.velocity.Z))
			stream.write(True)
			stream.write(c_float(transform.angular_velocity.X))
			stream.write(c_float(transform.angular_velocity.Y))
			stream.write(c_float(transform.angular_velocity.Z))
			stream.write(c_bit(False))
			if(type == game_enums.ReplicaTypes.SERIALIZATION):
				stream.write(c_bit(False))
		if(3 in object_components):
			if(type == game_enums.ReplicaTypes.SERIALIZATION):
				stream.write(c_bit(False))
				stream.write(c_float(0))
			stream.write(c_bit(False))
			stream.write(c_bit(True))
			transform = replica.get_component(components.Transform)
			stream.write(c_float(transform.position.X))
			stream.write(c_float(transform.position.Y))
			stream.write(c_float(transform.position.Z))
			stream.write(c_float(transform.rotation.X))
			stream.write(c_float(transform.rotation.Y))
			stream.write(c_float(transform.rotation.Z))
			stream.write(c_float(transform.rotation.W))
		if(20 in object_components):
			stream.write(c_bit(True))
			transform = replica.get_component(components.Transform)
			stream.write(c_float(transform.position.X))
			stream.write(c_float(transform.position.Y))
			stream.write(c_float(transform.position.Z))
			stream.write(c_float(transform.rotation.X))
			stream.write(c_float(transform.rotation.Y))
			stream.write(c_float(transform.rotation.Z))
			stream.write(c_float(transform.rotation.W))
		if(30 in object_components):
			vehicle_physics = replica.get_component(components.VehiclePhysics)
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_ubyte(vehicle_physics.data_1))
				stream.write(c_bit(vehicle_physics.flag_1))
			stream.write(c_bit(vehicle_physics.flag_2))
			if(vehicle_physics.flag_2 == True):
				stream.write(c_bit(vehicle_physics.flag_2_1))
		if(40 in object_components):
			stream.write(c_bit(True))
			transform = replica.get_component(components.Transform)
			stream.write(c_float(transform.position.X))
			stream.write(c_float(transform.position.Y))
			stream.write(c_float(transform.position.Z))
			stream.write(c_float(transform.rotation.X))
			stream.write(c_float(transform.rotation.Y))
			stream.write(c_float(transform.rotation.Z))
			stream.write(c_float(transform.rotation.W))
			physics_effect = replica.get_component(components.PhysicsEffect)
			if(physics_effect is not None):
				stream.write(c_bit(True))
				stream.write(c_ulong(physics_effect.effect_type))
				stream.write(c_float(physics_effect.effect_amount))
				stream.write(c_bit(False))
				stream.write(c_bit(True))
				stream.write(c_float(physics_effect.effect_direction.X))
				stream.write(c_float(physics_effect.effect_direction.Y))
				stream.write(c_float(physics_effect.effect_direction.Z))
			else:
				stream.write(c_bit(False))
		if(7 in object_components):
			destructible = replica.get_component(components.Destructible)
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_bit(destructible.flag_1))
				stream.write(c_bit(destructible.flag_2))


			stats = replica.get_component(components.Stats)
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_bit(False))
			stream.write(c_bit(True))
			stream.write(c_ulong(stats.health))
			stream.write(c_float(stats.max_health))
			stream.write(c_ulong(stats.armor))
			stream.write(c_float(stats.max_armor))
			stream.write(c_ulong(stats.imagination))
			stream.write(c_float(stats.max_imagination))
			stream.write(c_ulong(0))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_float(stats.max_health))
			stream.write(c_float(stats.max_armor))
			stream.write(c_float(stats.max_imagination))
			stream.write(c_ulong(1))
			stream.write(c_long(stats.faction))
			stream.write(c_bit(stats.is_smashable))
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_bit(False))
				stream.write(c_bit(False))
				if(stats.is_smashable == True):
					stream.write(c_bit(False))
					stream.write(c_bit(False))
		if(23 in object_components):
			stats = replica.get_component(components.Stats)
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_bit(False))
			stream.write(c_bit(True))
			stream.write(c_ulong(stats.health))
			stream.write(c_float(stats.max_health))
			stream.write(c_ulong(stats.armor))
			stream.write(c_float(stats.max_armor))
			stream.write(c_ulong(stats.imagination))
			stream.write(c_float(stats.max_imagination))
			stream.write(c_ulong(0))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_float(stats.max_health))
			stream.write(c_float(stats.max_armor))
			stream.write(c_float(stats.max_imagination))
			stream.write(c_ulong(1))
			stream.write(c_long(stats.faction))
			stream.write(c_bit(stats.is_smashable))
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_bit(False))
				stream.write(c_bit(False))
				if(stats.is_smashable == True):
					stream.write(c_bit(False))
					stream.write(c_bit(False))

			collectible = replica.get_component(components.Collectible)
			stream.write(c_ushort(collectible.collectible_id))
		if(26 in object_components):
			pet = replica.get_component(components.Pet)
			#TODO: Implement structure
			stream.write(c_bit(False))
		if(4 in object_components):
			character = replica.get_component(components.Character)
			minifig_comp = replica.get_component(components.Minifig)
			player, account = character.get_player_info()
			if(character.vehicle_id != 0):
				stream.write(c_bit(True))
				stream.write(c_bit(True))
				stream.write(c_longlong(character.vehicle_id))
				stream.write(c_ubyte(0))
			else:
				stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_bit(False))
				stream.write(c_bit(False))
				stream.write(c_bit(False))
				stream.write(c_bit(False))
				if(minifig_comp is not None):
					stream.write(c_ulong(minifig_comp.hair_color))
					stream.write(c_ulong(minifig_comp.hair_style))
					stream.write(c_ulong(0))
					stream.write(c_ulong(minifig_comp.chest))
					stream.write(c_ulong(minifig_comp.legs))
					stream.write(c_ulong(0))
					stream.write(c_ulong(0))
					stream.write(c_ulong(minifig_comp.eyebrows))
					stream.write(c_ulong(minifig_comp.eyes))
					stream.write(c_ulong(minifig_comp.mouth))
					stream.write(c_ulonglong(player["account_id"]))
					stream.write(c_ulonglong(0))
					stream.write(c_ulonglong(0))
					stream.write(c_ulonglong(player["Data"]["universe_score"]))
				else:
					stream.write(c_ulong(player["hair_color"]))
					stream.write(c_ulong(player["hair_style"]))
					stream.write(c_ulong(0))
					stream.write(c_ulong(player["shirt_color"]))
					stream.write(c_ulong(player["pants_color"]))
					stream.write(c_ulong(0))
					stream.write(c_ulong(0))
					stream.write(c_ulong(player["eyebrows"]))
					stream.write(c_ulong(player["eyes"]))
					stream.write(c_ulong(player["mouth"]))
					stream.write(c_ulonglong(player["account_id"]))
					stream.write(c_ulonglong(0))
					stream.write(c_ulonglong(0))
					stream.write(c_ulonglong(player["Data"]["universe_score"]))
				stream.write(c_bit(False))
				stats = player["Stats"]
				stream.write(c_longlong(stats["currency_collected"]))
				stream.write(c_longlong(stats["bricks_collected"]))
				stream.write(c_longlong(stats["smashables_smashed"]))
				stream.write(c_longlong(stats["quick_builds_done"]))
				stream.write(c_longlong(stats["enemies_smashed"]))
				stream.write(c_longlong(stats["rockets_used"]))
				stream.write(c_longlong(len(player["CompletedMissions"])))
				stream.write(c_longlong(stats["pets_tamed"]))
				stream.write(c_longlong(stats["imagination_collected"]))
				stream.write(c_longlong(stats["health_collected"]))
				stream.write(c_longlong(stats["armor_collected"]))
				stream.write(c_longlong(stats["distance_traveled"]))
				stream.write(c_longlong(stats["times_died"]))
				stream.write(c_longlong(stats["damage_taken"]))
				stream.write(c_longlong(stats["damage_healed"]))
				stream.write(c_longlong(stats["armor_repaired"]))
				stream.write(c_longlong(stats["imagination_restored"]))
				stream.write(c_longlong(stats["imagination_used"]))
				stream.write(c_longlong(stats["distance_driven"]))
				stream.write(c_longlong(stats["time_airborne_in_car"]))
				stream.write(c_longlong(stats["racing_imagination_collected"]))
				stream.write(c_longlong(stats["racing_imagination_crates_smashed"]))
				stream.write(c_longlong(stats["race_car_boosts"]))
				stream.write(c_longlong(stats["car_wrecks"]))
				stream.write(c_longlong(stats["racing_smashables_smashed"]))
				stream.write(c_longlong(stats["races_finished"]))
				stream.write(c_longlong(stats["races_won"]))
				stream.write(c_bit(False))
				stream.write(c_bit(False))#TODO: This is "is player landing by rocket", you need to implement it dummy
			stream.write(c_bit(True))
			stream.write(c_bit(replica.zone.pvp_enabled))
			stream.write(c_bit(bool(account["is_admin"])))
			stream.write(c_ubyte(character.gm_level))
			stream.write(c_bit(False))
			stream.write(c_ubyte(0))
			stream.write(c_bit(True))
			stream.write(c_ulong(character.head_glow))
			stream.write(c_bit(False))#TODO: This has to do with guilds, should eventually be implemented
		if(19 in object_components):
			pass
		if(17 in object_components):
			inventory = replica.get_component(components.Inventory)
			stream.write(c_bit(True))
			stream.write(c_ulong(len(inventory.items)))
			for item in inventory.items:
				stream.write(c_longlong(item["item_id"]))
				stream.write(c_long(item["lot"]))
				stream.write(c_bit(False))
				stream.write(c_bit(True))
				stream.write(c_ulong(item["quantity"]))
				stream.write(c_bit(True))
				stream.write(c_ulong(item["slot"]))
				stream.write(c_bit(False))
				stream.write(c_bit(False))#TODO: Implement this, not entirely sure what its for
				stream.write(c_bit(True))
			stream.write(c_bit(False))
		if(5 in object_components):
			stream.write(c_bit(False))#TODO: Implement Script Component
		if(9 in object_components):
			stream.write(c_bit(False))#TODO: Implement Skill Component
		if(60 in object_components):
			base_combat_ai = replica.get_component(components.BaseCombatAI)
			stream.write(c_bit(True))
			stream.write(c_ulong(base_combat_ai.action))
			stream.write(c_longlong(base_combat_ai.target_id))
		if(48 in object_components):#TODO: Implment Rebuild Component
			stream.write(c_bit(False))

			stats = replica.get_component(components.Stats)
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_bit(False))
			stream.write(c_bit(True))
			stream.write(c_ulong(stats.health))
			stream.write(c_float(stats.max_health))
			stream.write(c_ulong(stats.armor))
			stream.write(c_float(stats.max_armor))
			stream.write(c_ulong(stats.imagination))
			stream.write(c_float(stats.max_imagination))
			stream.write(c_ulong(0))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_float(stats.max_health))
			stream.write(c_float(stats.max_armor))
			stream.write(c_float(stats.max_imagination))
			stream.write(c_ulong(1))
			stream.write(c_long(stats.faction))
			stream.write(c_bit(stats.is_smashable))
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_bit(False))
				stream.write(c_bit(False))
				if(stats.is_smashable == True):
					stream.write(c_bit(False))
					stream.write(c_bit(False))
		if(25 in object_components):#TODO: Implement Moving Platforms
			stream.write(c_bit(False))
		if(49 in object_components):
			switch = replica.get_component(components.Switch)
			stream.write(c_bit(switch.state))
		if(16 in object_components):#TODO: Implement Vendors
			stream.write(c_bit(False))
		if(6 in object_components):
			bouncer = replica.get_component(components.Bouncer)
			stream.write(c_bit(True))
			stream.write(c_bit(not bouncer.pet_required))
		if(39 in object_components):#TODO Implement Scripted Activity
			stream.write(c_bit(False))
		if(71 in object_components):
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
			stream.write(c_bit(False))
		if(75 in object_components):
			exhibit = replica.get_component(components.LUPExhibit)
			stream.write(c_bit(True))
			stream.write(c_long(exhibit.exhibited_lot))
		if(42 in object_components):
			pass#This is apparently not even needed?
		if(2 in object_components):
			if(type == game_enums.ReplicaTypes.CONSTRUCTION):
				stream.write(c_ulong(0))#TODO: Implement render component
		if(107 in object_components):
			stream.write(c_bit(False))
		if(69 in object_components):
			trigger = replica.get_component(components.Trigger)
			stream.write(c_bit(True))
			stream.write(c_long(trigger.trigger_id))

















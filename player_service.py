import services
import json
import database
import copy
import game_enums
import typing
import time
import threading
import game_types

class PlayerService(services.GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Player"

		self._accounts = []

		global game
		game = self.get_parent()

	def initialize(self):
		super().initialize()
		def sync_thread():
			while True:
				self.sync_database()
				time.sleep(1)
		sync = threading.Thread(target=sync_thread)
		sync.start()

	def add_account(self, account_id : int):
		server_db = self.get_parent().get_service("Database").server_db
		
		c = server_db.connection.cursor()
		
		c.execute("SELECT * FROM Accounts WHERE account_id = ?", (account_id,))
		account = c.fetchone()
		c.execute("SELECT * FROM Characters WHERE account_id = ?", (account_id,))
		characters = c.fetchall()
		for character in characters:
			c.execute("SELECT * FROM CharacterData WHERE player_id = ?", (character["player_id"],))
			data = c.fetchone()
			data["position"] = game_types.Vector3(str_val=data["position"])
			data["rotation"] = game_types.Vector4(str_val=data["rotation"])
			character["Data"] = data
			c.execute("SELECT * FROM CharacterStats WHERE player_id = ?", (character["player_id"],))
			character["Stats"] = c.fetchone()
			c.execute("SELECT * FROM CompletedMissions WHERE player_id = ?", (character["player_id"],))
			character["CompletedMissions"] = c.fetchall()
			c.execute("SELECT * FROM CurrentMissions WHERE player_id = ?", (character["player_id"],))
			character["CurrentMissions"] = c.fetchall()
			c.execute("SELECT * FROM Inventory WHERE player_id = ?", (character["player_id"],))
			inventory = c.fetchall()
			for item in inventory:
				if(item["json"] is not None):
					item["json"] = json.loads(item["json"])
				else:
					item["json"] = {}
			character["Inventory"] = inventory
		account["Characters"] = characters
		self._accounts.append(account)
		self.get_parent().trigger_event("AccountAdded", args=(account,))

	def remove_account(self, account_id : int):
		for account in self._accounts:
			if(account["account_id"] == account_id):
				self._accounts.remove(account)

	def sync_database(self, accounts : typing.Iterable = None):
		if(accounts is None):
			accounts = self._accounts
		server_db = self.get_parent().get_service("Database").server_db
		c = server_db.connection.cursor()

		for account in accounts:
			account_copy = copy.deepcopy(account)
			for character in account_copy["Characters"]:
				inventory = copy.deepcopy(character["Inventory"])
				del character["Inventory"]
				stats = copy.deepcopy(character["Stats"])
				del character["Stats"]
				data = copy.deepcopy(character["Data"])
				data["position"] = str(data["position"])
				data["rotation"] = str(data["rotation"])
				del character["Data"]
				completed_missions = character["CompletedMissions"]
				del character["CompletedMissions"]
				current_missions = character["CurrentMissions"]
				del character["CurrentMissions"]

				c.execute("UPDATE Characters SET name = ?, zone = ?, shirt_color = ?, shirt_style = ?, pants_color = ?, hair_color = ?, hair_style = ?, lh = ?, rh = ?, eyebrows = ?, eyes = ?, mouth = ? WHERE player_id = ?",
						  (character["name"], character["zone"], character["shirt_color"], character["shirt_style"], character["pants_color"], character["hair_color"], character["hair_style"], character["lh"], character["rh"],
						   character["eyebrows"], character["eyes"], character["mouth"], character["player_id"]))
				c.execute('''UPDATE CharacterStats SET currency_collected = ?, bricks_collected = ?, smashables_smashed = ?, quick_builds_done = ?, enemies_smashed = ?, rockets_used = ?, pets_tamed = ?, imagination_collected = ?, health_collected = ?, armor_collected = ?, distance_traveled = ?, times_died = ?,
						  damage_taken = ?, damage_healed = ?, armor_repaired = ?, imagination_restored = ?, imagination_used = ?, distance_driven = ?, time_airborne_in_car = ?, racing_imagination_collected = ?, racing_imagination_crates_smashed = ?, race_car_boosts = ?, car_wrecks = ?, racing_smashables_smashed = ?,
						  races_finished = ?, races_won = ? WHERE player_id = ?''', (stats["currency_collected"], stats["bricks_collected"], stats["smashables_smashed"], stats["quick_builds_done"], stats["enemies_smashed"], stats["rockets_used"], stats["pets_tamed"], stats["imagination_collected"], stats["health_collected"], stats["armor_collected"], stats["distance_traveled"], stats["times_died"],
						  stats["damage_taken"], stats["damage_healed"], stats["armor_repaired"], stats["imagination_restored"], stats["imagination_used"], stats["distance_driven"], stats["time_airborne_in_car"], stats["racing_imagination_collected"], stats["racing_imagination_crates_smashed"], stats["race_car_boosts"], stats["car_wrecks"], stats["racing_smashables_smashed"],
						  stats["races_finished"], stats["races_won"], character["player_id"]))
				c.execute('''UPDATE CharacterData SET universe_score = ?, level = ?, health = ?, max_health = ?, armor = ?, max_armor = ?, imagination = ?, max_imagination = ?, currency = ?, position = ?, rotation = ?, backpack_space = ? WHERE player_id = ?''',
						  (data["universe_score"], data["level"], data["health"], data["max_health"], data["armor"], data["max_armor"], data["imagination"], data["max_imagination"], data["currency"], data["position"], data["rotation"], data["backpack_space"], character["player_id"]))

				for mission in completed_missions:
					c.execute("SELECT * FROM CompletedMissions WHERE player_id = ? and mission_id = ?", (mission["player_id"], mission["mission_id"]))
					check = c.fetchall()
					if(check == []):
						c.execute("INSERT INTO CompletedMissions (player_id, mission_id) VALUES (?, ?)", (mission["player_id"], mission["mission_id"]))

				for mission in current_missions:
					c.execute("SELECT * FROM CurrentMissions WHERE player_id = ? and mission_id = ?", (mission["player_id"], mission["mission_id"]))
					check = c.fetchall()
					if(check == []):
						c.execute("INSERT INTO CurrentMissions (player_id, mission_id, progress) VALUES (?, ?, ?)", (mission["player_id"], mission["mission_id"], mission["progress"]))
					else:
						c.execute("UPDATE CurrentMissions SET progress = ? WHERE player_id = ? AND mission_id = ?", (mission["progress"], mission["player_id"], mission["mission_id"]))

				c.execute("SELECT * FROM CurrentMissions WHERE player_id = ?", (character["player_id"],))
				db_missions = c.fetchall()
				for mission in db_missions:
					keep = False
					for server_mission in current_missions:
						if(server_mission["mission_id"] == mission["mission_id"]):
							keep = True
					if(keep == False):
						c.execute("DELETE FROM CurrentMissions WHERE player_id = ? AND mission_id = ?", (mission["player_id"], mission["mission_id"]))

				for item in inventory:
					item["json"] = json.dumps(item["json"])
					c.execute("SELECT * FROM Inventory WHERE item_id = ?", (item["item_id"],))
					check = c.fetchall()
					if(check == []):
						c.execute("INSERT INTO Inventory (lot, slot, equipped, linked, quantity, item_id, player_id, json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
								  (item["lot"], item["slot"], item["equipped"], item["linked"], item["quantity"], item["item_id"], item["player_id"], item["json"]))
					else:
						c.execute("UPDATE Inventory SET slot = ?, equipped = ?, linked = ?, quantity = ?, json = ? WHERE item_id = ?",
								  (item["slot"], item["equipped"], item["linked"], item["quantity"], item["json"], item["item_id"]))

				c.execute("SELECT * FROM Inventory WHERE player_id = ?", (character["player_id"],))
				db_inventory = c.fetchall()
				for item in db_inventory:
					keep = False
					for server_item in inventory:
						if(server_item["item_id"] == item["item_id"]):
							keep = True
					if(keep == False):
						c.execute("DELETE FROM Inventory WHERE item_id = ?", (item["item_id"],))


	def delete_player(self, player_id):
		account = self.get_account_by_player_id(player_id)
		self.sync_database(accounts=[account])
		player = copy.deepcopy(self.get_player_by_id(player_id))

		for character in account["Characters"]:
			if(character["player_id"] == player_id):
				account["Characters"].remove(character)

		db = self.get_parent().get_service("Database").server_db
		c = db.connection.cursor()

		c.execute("DELETE FROM Characters WHERE player_id = ?", (player_id,))
		c.execute("DELETE FROM CharacterData WHERE player_id = ?", (player_id,))
		c.execute("DELETE FROM CharacterStats WHERE player_id = ?", (player_id,))
		c.execute("DELETE FROM CompletedMissions WHERE player_id = ?", (player_id,))
		c.execute("DELETE FROM CurrentMissions WHERE player_id = ?", (player_id,))
		c.execute("DELETE FROM Inventory WHERE player_id = ?", (player_id,))

		self.get_parent().trigger_event("PlayerDeleted", args=(player,))

	def create_player(self, account_id : int, name: str, shirt_color: int, shirt_style: int, pants_color: int, hair_color: int,
						 hair_style: int, lh: int, rh: int, eyebrows: int, eyes: int, mouth: int, custom_name: str):
		db = self.get_parent().get_service("Database").server_db
		c = db.connection.cursor()

		player_id = self.get_parent().generate_object_id()

		c.execute('''INSERT INTO CharacterStats (currency_collected, bricks_collected, smashables_smashed, quick_builds_done, enemies_smashed, rockets_used, pets_tamed, imagination_collected, health_collected, armor_collected, distance_traveled, times_died,
				  damage_taken, damage_healed, armor_repaired, imagination_restored , imagination_used, distance_driven, time_airborne_in_car, racing_imagination_collected, racing_imagination_crates_smashed, race_car_boosts, car_wrecks, racing_smashables_smashed,
				  races_finished, races_won, player_id) VALUES (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,?)''', (player_id,))
		c.execute('''INSERT INTO Characters (account_id, name, shirt_color, shirt_style, pants_color, hair_color, hair_style, lh, rh, eyebrows, eyes, mouth, zone, player_id, custom_name) VALUES
				  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (account_id, name, shirt_color, shirt_style, pants_color, hair_color, hair_style, lh, rh, eyebrows, eyes, mouth, 1000, player_id, custom_name))
		c.execute('''INSERT INTO CharacterData (universe_score, level, health, max_health, armor, max_armor, imagination, max_imagination, currency, position, rotation, player_id, backpack_space) VALUES
			  	  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (0, 0, 4, 4, 0, 0, 0, 0, 0, "0,0,0", "0,0,0", player_id, 20))



		account = self.get_account_by_id(account_id)
		self.sync_database([account])
		player_copy = copy.deepcopy({"account_id":account_id, "name":name, "shirt_color":shirt_color, "shirt_style":shirt_style, "pants_color":pants_color, "hair_color":hair_color, "hair_style":hair_style,
								"lh":lh, "rh":rh, "eyebrows":eyebrows, "eyes":eyes, "mouth":mouth, "zone":1000, "player_id":player_id, "custom_name":custom_name})
		player_copy["Data"] = {"universe_score":0, "level":0, "health":4, "max_health":4, "armor":0, "max_armor":0, "imagination":0, "max_imagination":0, "currency":0, "position":"0,0,0",
									 "rotation":"0,0,0,0", "player_id":player_id, "backpack_space":20}
		player_copy["Data"]["position"] = game_types.Vector3(str_val = player_copy["Data"]["position"])
		player_copy["Data"]["rotation"] = game_types.Vector4(str_val = player_copy["Data"]["rotation"])
		player_copy["Stats"] = {"currency_collected":0, "bricks_collected":0, "smashables_smashed":0, "quick_builds_done":0, "enemies_smashed":0, "rockets_used":0, "pets_tamed":0,
									  "imagination_collected":0, "health_collected":0, "armor_collected":0, "distance_traveled":0, "times_died":0, "damage_taken":0, "damage_healed":0,
									  "armor_repaired":0, "imagination_restored":0, "imagination_used":0, "distance_driven":0, "time_airborne_in_car":0, "racing_imagination_collected":0,
									  "racing_imagination_crates_smashed":0, "race_car_boosts":0, "car_wrecks":0, "racing_smashables_smashed":0, "races_finished":0, "races_won":0, "player_id":player_id}
		player_copy["CompletedMissions"] = []
		player_copy["CurrentMissions"] = []
		player_copy["Inventory"] = []
		account["Characters"].append(player_copy)
		self.get_parent().trigger_event("PlayerCreated", args=[player_id,])

		shirt_id = 0
		if (shirt_color == 0):
			if (shirt_style >= 35):
				shirt_id = 5730
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_BRIGHT_RED.value
		elif (shirt_color == 1):
			if (shirt_style >= 35):
				shirt_id = 5736
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_BRIGHT_BLUE.value
		elif (shirt_color == 3):
			if (shirt_style >= 35):
				shirt_id = 5808
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_DARK_GREEN.value
		elif (shirt_color == 5):
			if (shirt_style >= 35):
				shirt_id = 5754
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_BRIGHT_ORANGE.value
		elif (shirt_color == 6):
			if (shirt_style >= 35):
				shirt_id = 5760
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_BLACK.value
		elif (shirt_color == 7):
			if (shirt_style >= 35):
				shirt_id = 5766
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_DARK_STONE_GRAY.value
		elif (shirt_color == 8):
			if (shirt_style >= 35):
				shirt_id = 5772
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_MEDIUM_STONE_GRAY.value
		elif (shirt_color == 9):
			if (shirt_style >= 35):
				shirt_id = 5778
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_REDDISH_BROWN.value
		elif (shirt_color == 10):
			if (shirt_style >= 35):
				shirt_id = 5784
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_WHITE.value
		elif (shirt_color == 11):
			if (shirt_style >= 35):
				shirt_id = 5802
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_MEDIUM_BLUE.value
		elif (shirt_color == 13):
			if (shirt_style >= 35):
				shirt_id = 5796
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_DARK_RED.value
		elif (shirt_color == 14):
			if (shirt_style >= 35):
				shirt_id = 5802
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_EARTH_BLUE.value
		elif (shirt_color == 15):
			if (shirt_style >= 35):
				shirt_id = 5808
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_EARTH_GREEN.value
		elif (shirt_color == 16):
			if (shirt_style >= 35):
				shirt_id = 5814
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_BRICK_YELLOW.value
		elif (shirt_color == 84):
			if (shirt_style >= 35):
				shirt_id = 5820
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_SAND_BLUE.value
		elif (shirt_color == 96):
			if (shirt_style >= 35):
				shirt_id = 5826
			else:
				shirt_id = game_enums.ItemLOTs.SHIRT_SAND_GREEN.value

		if (shirt_style >= 35):
			final_shirt_id = shirt_id + (shirt_style - 35)
		else:
			final_shirt_id = shirt_id + (shirt_style - 1)

		if (pants_color == 0):
			pants_id = game_enums.ItemLOTs.PANTS_BRIGHT_RED.value
		elif (pants_color == 1):
			pants_id = game_enums.ItemLOTs.PANTS_BRIGHT_BLUE.value
		elif (pants_color == 3):
			pants_id = game_enums.ItemLOTs.PANTS_DARK_GREEN.value
		elif (pants_color == 5):
			pants_id = game_enums.ItemLOTs.PANTS_BRIGHT_ORANGE.value
		elif (pants_color == 6):
			pants_id = game_enums.ItemLOTs.PANTS_BLACK.value
		elif (pants_color == 7):
			pants_id = game_enums.ItemLOTs.PANTS_DARK_STONE_GRAY.value
		elif (pants_color == 8):
			pants_id = game_enums.ItemLOTs.PANTS_MEDIUM_STONE_GRAY.value
		elif (pants_color == 9):
			pants_id = game_enums.ItemLOTs.PANTS_REDDISH_BROWN.value
		elif (pants_color == 10):
			pants_id = game_enums.ItemLOTs.PANTS_WHITE.value
		elif (pants_color == 11):
			pants_id = game_enums.ItemLOTs.PANTS_MEDIUM_BLUE.value
		elif (pants_color == 13):
			pants_id = game_enums.ItemLOTs.PANTS_DARK_RED.value
		elif (pants_color == 14):
			pants_id = game_enums.ItemLOTs.PANTS_EARTH_BLUE.value
		elif (pants_color == 15):
			pants_id = game_enums.ItemLOTs.PANTS_EARTH_GREEN.value
		elif (pants_color == 16):
			pants_id = game_enums.ItemLOTs.PANTS_BRICK_YELLOW.value
		elif (pants_color == 84):
			pants_id = game_enums.ItemLOTs.PANTS_SAND_BLUE.value
		elif (pants_color == 96):
			pants_id = game_enums.ItemLOTs.PANTS_SAND_GREEN.value
		else:
			pants_id = 2508

		self.add_item_to_inventory(player_id, final_shirt_id, equipped=True, linked=True, json_data={"from":"character_creation"})
		self.add_item_to_inventory(player_id, pants_id, equipped=True, linked=True,json_data={"from":"character_creation"})

	def get_account_by_id(self, account_id : int):
		for account in self._accounts:
			if(account["account_id"] == account_id):
				return account
		return None

	def get_player_object_by_id(self, player_id : int):
		session = self.get_parent().get_service("Session").get_session_by_player_id(player_id)
		zone = self.get_parent().get_service("World").get_zone_by_id(session.zone_id)
		return zone.get_object_by_id(player_id)


	def get_account_by_player_id(self, player_id : int):
		for account in self._accounts:
			for character in account["Characters"]:
				if(character["player_id"] == player_id):
					return account
		return None

	def get_player_by_id(self, player_id : int):
		for account in self._accounts:
			for character in account["Characters"]:
				if(character["player_id"] == player_id):
					return character
		return None

	def add_item_to_inventory(self, player_id : int, lot : int, slot : int = None, equipped : bool = False, linked : bool = False, quantity : int = 1, json_data : dict = None):
		if(json_data is None):
			json_data = {}
		player = self.get_player_by_id(player_id)
		if(slot is None):
			availible_slots = []
			for i in range(player["Data"]["backpack_space"]):
				availible_slots.append(i)
			for item in player["Inventory"]:
				availible_slots.remove(item["slot"])
			if(availible_slots != []):
				slot = availible_slots[0]
			else:
				print("No Inventory Space Availible!")
				return None

		database_service = game.get_service("Database")
		cdclient = database_service.cdclient_db
		c = cdclient.connection.cursor()

		c.execute("SELECT component_id FROM ComponentsRegistry WHERE id = ? and component_type = 11", (lot,))
		item_component_id = c.fetchone()
		c.execute("SELECT * FROM ItemComponent WHERE id = ?", (item_component_id["component_id"],))
		item_data = c.fetchone()

		new_item_id = game.generate_object_id()

		json_data["proxy_items"] = []
		if(item_data["subItems"] is not None):
			json_data["proxy_items"].append({"player_id":player_id, "lot":int(item_data["subItems"]), "slot":-1, "equipped":1, "linked":1, "quantity":1, "item_id":game.generate_object_id(), "json":{"is_proxy":1, "parent_item":new_item_id}})

		item = {"player_id":player_id, "lot":lot, "slot":slot, "equipped":int(equipped), "linked":int(linked), "quantity":quantity, "json":json_data, "item_id":new_item_id}

		db = self.get_parent().get_service("Database").server_db
		c2 = db.connection.cursor()
		db_item = copy.deepcopy(item)
		db_item["json"] = json.dumps(db_item["json"])
		c2.execute("INSERT INTO Inventory (lot, slot, equipped, linked, quantity, item_id, player_id, json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
			(db_item["lot"], db_item["slot"], db_item["equipped"], db_item["linked"], db_item["quantity"], db_item["item_id"], db_item["player_id"], db_item["json"]))

		player["Inventory"].append(item)
		self.get_parent().trigger_event("ItemAdded", args=[player_id, item])
		return item

	def get_item_by_id(self, player_id : int, item_id : int):
		player = self.get_player_by_id(player_id)
		if(player is not None):
			for item in player["Inventory"]:
				if(item["item_id"] == item_id):
					return item
		return None

	def get_equipped_items(self, player_id : int):
		player = self.get_player_by_id(player_id)
		items = []
		def parse_item(item):
			if (int(item["equipped"]) == 1):
				items.append(item)
				if ("proxy_items" in item["json"] and item["json"]["proxy_items"] != []):
					for proxy_item in item["json"]["proxy_items"]:
						parse_item(proxy_item)
		for item in player["Inventory"]:
			parse_item(item)
		self.get_parent().trigger_event("EquipListRequest", args=[player_id, items])
		return items












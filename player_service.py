import services
import json
import database
import copy
import game_enums

class PlayerService(services.GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Player"

		self._accounts = []

	def add_account(self, account_id : int):
		db = self.get_parent().get_service("Database").server_db

		account_table = db.tables["Accounts"]
		character_table = db.tables["Characters"]
		character_data_table = db.tables["CharacterData"]
		character_stats_table = db.tables["CharacterStats"]
		completed_missions_table = db.tables["CompletedMissions"]
		current_missions_table = db.tables["CurrentMissions"]
		inventory_table = db.tables["Inventory"]


		account = account_table.select(["account_id", "username", "banned", "is_admin"], "account_id = {}".format(account_id))[0]
		characters = character_table.select_all("account_id = {}".format(account_id))
		for character in characters:
			character["Data"] = character_data_table.select_all("player_id = {}".format(character["player_id"]))
			character["Stats"] = character_stats_table.select_all("player_id = {}".format(character["player_id"]))
			character["CompletedMissions"] = completed_missions_table.select_all("player_id = {}".format(character["player_id"]))
			character["CurrentMissions"] = current_missions_table.select_all("player_id = {}".format(character["player_id"]))
			inventory = inventory_table.select_all("player_id = {}".format(character["player_id"]))
			for item in inventory:
				if(item["json"] is not None):
					item["json"] = json.loads(item["json"])
				else:
					item["json"] = {}
			character["Inventory"] = inventory
		account["Characters"] = characters
		self._accounts.append(account)

	def remove_account(self, account_id : int):
		for account in self._accounts:
			if(account["account_id"] == account_id):
				self._accounts.remove(account)

	def create_player(self, account_id : int, name: str, shirt_color: int, shirt_style: int, pants_color: int, hair_color: int,
						 hair_style: int, lh: int, rh: int, eyebrows: int, eyes: int, mouth: int):
		db = self.get_parent().get_service("Database").server_db
		character_table : database.DBTable = db.tables["Characters"]
		character_data_table : database.DBTable = db.tables["CharacterData"]
		character_stats_table : database.DBTable = db.tables["CharacterStats"]

		player_id = self.get_parent().generate_object_id()
		player_base = {"account_id":account_id, "name":name, "shirt_color":shirt_color, "shirt_style":shirt_style, "pants_color":pants_color, "hair_color":hair_color, "hair_style":hair_style,
								"lh":lh, "rh":rh, "eyebrows":eyebrows, "eyes":eyes, "mouth":mouth, "zone":0, "player_id":player_id}
		player_data = {"universe_score":0, "level":0, "health":4, "max_health":4, "armor":0, "max_armor":0, "imagination":0, "max_imagination":0, "currency":0, "position":"0,0,0",
									 "rotation":"0,0,0,0", "player_id":player_id}
		player_stats = {"currency_collected":0, "bricks_collected":0, "smashables_smashed":0, "quick_builds_done":0, "enemies_smashed":0, "rockets_used":0, "pets_tamed":0,
									  "imagination_collected":0, "health_collected":0, "armor_collected":0, "distance_traveled":0, "times_died":0, "damage_taken":0, "damage_healed":0,
									  "armor_repaired":0, "imagination_restored":0, "imagination_used":0, "distance_driven":0, "time_airborne_in_car":0, "racing_imagination_collected":0,
									  "racing_imagination_crates_smashed":0, "race_car_boosts":0, "car_wrecks":0, "racing_smashables_smashed":0, "races_finished":0, "races_won":0, "player_id":player_id}

		character_table.insert(player_base)
		character_data_table.insert(player_data)
		character_stats_table.insert(player_stats)


		self.remove_account(account_id)
		self.add_account(account_id)
		self.get_parent().trigger_event("CharacterCreated", args=[player_id,])

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

		self.add_item_to_inventory(player_id, final_shirt_id, equipped=True, linked=True, json_data={"from_character_creation":1})
		self.add_item_to_inventory(player_id, pants_id, equipped=True, linked=True,json_data={"from_character_creation": 1})



	def get_account_by_id(self, account_id : int):
		for account in self._accounts:
			if(account["account_id"] == account_id):
				return account
		return None

	def get_account_from_player_id(self, player_id : int):
		for account in self._accounts:
			for character in account["Characters"]:
				if(character["player_id"] == player_id):
					return account
		return None

	def get_player_from_id(self, player_id : int):
		for account in self._accounts:
			for character in account["Characters"]:
				if(character["player_id"] == player_id):
					return character
		return None

	def add_item_to_inventory(self, player_id : int, lot : int, slot : int = None, equipped : bool = False, linked : bool = False, quantity : int = 1, json_data : dict = None):
		if(json_data is None):
			json_data = {}
		player = self.get_player_from_id(player_id)
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
				return
		item = {"player_id":player_id, "lot":lot, "slot":slot, "equipped":int(equipped), "linked":int(linked), "quantity":quantity, "json":json_data, "item_id":self.get_parent().generate_object_id()}
		db = self.get_parent().get_service("Database").server_db
		inventory_table = db.tables["Inventory"]
		db_item = copy.deepcopy(item)
		db_item["json"] = json.dumps(db_item["json"])
		inventory_table.insert(db_item)

		player["Inventory"].append(item)
		self.get_parent().trigger_event("ItemAdded", args=[player_id, item])

	def get_equipped_items(self, player_id : int):
		player = self.get_player_from_id(player_id)
		inventory = player["Inventory"]
		items = []
		for item in inventory:
			if(item["equipped"] == 1):
				items.append(item)
		return items












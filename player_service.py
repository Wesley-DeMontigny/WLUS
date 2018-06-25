import services
import json

class PlayerService(services.GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Player"

		self._accounts = []

	def add_account(self, account_id):
		database = self.get_parent().get_service("Database").server_db

		account_table = database.tables["Accounts"]
		character_table = database.tables["Characters"]
		character_config_table = database.tables["CharacterConfig"]
		character_stats_table = database.tables["CharacterStatistics"]
		completed_missions_table = database.tables["CompletedMissions"]
		current_missions_table = database.tables["CurrentMissions"]
		inventory_table = database.tables["Inventory"]


		account = account_table.select(["AccountID", "Username", "Banned", "IsAdmin"], "AccountID = {}".format(account_id))[0]
		characters = character_table.select_all("AccountID = {}".format(account_id))
		for character in characters:
			character["Config"] = character_config_table.select_all("PlayerID = {}".format(character["ObjectID"]))
			character["Stats"] = character_stats_table.select_all("PlayerID = {}".format(character["ObjectID"]))
			character["CompletedMissions"] = completed_missions_table.select_all("PlayerID = {}".format(character["ObjectID"]))
			character["CurrentMissions"] = current_missions_table.select_all("PlayerID = {}".format(character["ObjectID"]))
			inventory = inventory_table.select_all("OwnerID = {}".format(character["ObjectID"]))
			for item in inventory:
				item["JSON"] = json.load(item["JSON"])[0]
			character["Inventory"] = inventory
		account["Characters"] = characters
		self._accounts.append(account)

	def get_account_by_id(self, account_id):
		for account in self._accounts:
			if(account["AccountID"] == account_id):
				return account
		return None

	def get_account_from_player_id(self, player_id):
		for account in self._accounts:
			for character in account["Characters"]:
				if(character["ObjectID"] == player_id):
					return account
		return None

	def get_player_from_id(self, player_id):
		for account in self._accounts:
			for character in account["Characters"]:
				if(character["ObjectID"] == player_id):
					return character
		return None

	def get_equipped_items(self, player_id):
		player = self.get_player_from_id(player_id)
		inventory = player["Inventory"]
		items = []
		for item in inventory:
			if(item["Equipped"] == 1):
				items.append(item)
		return items












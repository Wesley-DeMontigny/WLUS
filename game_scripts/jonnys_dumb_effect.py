import sys
sys.path.append("..")
import scripts
import time

'''Big thanks to Tracer (the other Wesley), for providing me with the function from JALUS that does this thing'''

class Main(scripts.Script):
	def __init__(self, parent):
		super().__init__(parent, "Jonny's Dumb Effect")
		global game
		game = self.get_parent()

	def run(self):
		game.wait_for_event("ServiceInitialized", '''args[0].get_name() == "World"''')
		game_message_service = game.get_service("Game Message")
		while True:
			if (game.get_config("jonnys_dumb_effect") is not None and game.get_config("jonnys_dumb_effect") == True):
				zones = game.get_service("World").get_zones()
				for zone in zones:
					players = zone.get_players()
					for player_id in players:
						game_message_service.stop_fx_effect(player_id, zone.get_connections(), False, "wisp_hands")
						game_message_service.play_fx_effect(player_id, zone.get_connections(), 1573, "on-anim", 1.0, "wisp_hands")

						game_message_service.stop_fx_effect(player_id, zone.get_connections(), False, "wisp_hands_left")
						game_message_service.play_fx_effect(player_id, zone.get_connections(), 1579, "on-anim", 1.0, "wisp_hands_left")

				time.sleep(.5)

import game
import services
import scripts
import session_service
import os
import asyncio
import configparser
import player_service
import time

if __name__ == "__main__":
	game = game.Game()

	config = configparser.ConfigParser()
	config.read("config.ini")
	game_config = config["GAME_CONFIG"]
	game.set_config("address", str(game_config["address"]))
	game.set_config("auth_port", int(game_config["auth_port"]))
	game.set_config("world_port", int(game_config["world_port"]))
	game.set_config("auth_max_connections", int(game_config["auth_max_connections"]))
	game.set_config("world_max_connections", int(game_config["world_max_connections"]))

	#Append all game scripts to Game
	for file in os.listdir("./game_scripts"):
		if file.endswith(".py"):
			game.add_script(scripts.Script(game, file, "./game_scripts/"+file))

	database = services.DatabaseService(game)
	game.register_service(database)

	player = player_service.PlayerService(game)
	game.register_service(player)

	session = session_service.SessionService(game)
	game.register_service(session)

	auth_server = services.AuthServerService(game)
	game.register_service(auth_server)

	world = services.WorldService(game)
	game.register_service(world)

	world_server = services.WorldServerService(game)
	game.register_service(world_server)

	game.start()

	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()
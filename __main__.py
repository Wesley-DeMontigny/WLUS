import game
import services
import scripts
import sessions
import asyncio

if __name__ == "__main__":
	game = game.Game()

	game.set_config("address", "127.0.0.1")
	game.set_config("auth_port", "1001")
	game.set_config("world_port", "2002")

	database = services.DatabaseService(game)
	game.register_service(database)

	session = sessions.SessionService(game)
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
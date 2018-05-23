import AuthServer
from GameManager import GameManager
import asyncio
import WorldServer

if __name__ == "__main__":

	GM = GameManager()

	AuthServer.AuthServer(("localhost", 1001), max_connections=10, incoming_password=b"3.25 ND1", GameManager=GM)
	WorldServer.WorldServer(("localhost", 2002), max_connections=10, incoming_password=b"3.25 ND1", GameManager=GM)

	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()
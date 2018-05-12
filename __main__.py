from World import *
from Auth import *
from DBHandlers import *

if __name__ == "__main__":
	DBServerStarup()

	DB_Manager = databaseManager()

	World = WorldServer(("127.0.0.1", 2002), DB_Manager, max_connections=10, incoming_password=b"3.25 ND1",
							 role="WORLD")
	Auth = AuthServer(("127.0.0.1", 1001), DB_Manager, max_connections=10, incoming_password=b"3.25 ND1",
						   role="AUTH")

	loop = asyncio.get_event_loop()
	loop.run_forever()
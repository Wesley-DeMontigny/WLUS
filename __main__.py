"""
This is the file that is used to start various servers.
Command Line Arguments: <mode> <port> <zone> <name>
    mode - This determines what will run. There are technically  infinite options.
           What actually determines what happens are the plugins that are of that same type.
           "Master" is a special type though -- it starts the master server. There are no plugins for the master server.
           To use a combination of server types like a Char and World server use a '-' between the types
            Example: char-world
    port - Port for the server
    zone - If there's no zone just put 'None' otherwise use the zone id of the world file you want to load
    name - The name of the instance (don't use spaces)
"""
import sys
import configparser
from core import generic_game_server, master_server
import asyncio
sys.path.append("./plugins")


if __name__ == "__main__":

    if len(sys.argv) == 5 and str(sys.argv[1]).lower() != "master":
        config = configparser.ConfigParser()
        config.read("config.ini")
        generic_game_server.GameServer((config["GENERAL"]["bind_address"], int(sys.argv[2])), max_connections=5,
                                       incoming_password=b"3.25 ND1", server_type=str(sys.argv[1]).lower(),
                                       zone=eval(sys.argv[3]), name=sys.argv[4])
        print(f"Started WLUS Instance '{sys.argv[4]}'\n   Type: [{sys.argv[1].lower()}]\n   Port: [{sys.argv[2]}]\n"
              f"   Zone: [{eval(sys.argv[3])}]")
        loop = asyncio.get_event_loop()
        loop.run_forever()
        loop.close()
    elif len(sys.argv) == 3:
        server = master_server.MasterServer(('0.0.0.0', int(sys.argv[2])))
    else:
        print("Missing arguments")

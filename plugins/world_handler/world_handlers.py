"""
This will handle all of the character related packets.
"""
from ..serializables import packet_enum, world_to_client, client_to_world, global_packets, misc_serializables
from pyraknet.bitstream import *
from ..char_handler import char_handlers


class Plugin:
    def __init__(self, parent):
        print("World Handler Initiated")
        parent.register_handler(char_handlers.Plugin.handle_minifigure_list_request,
                                packet_enum.PacketHeader.CLIENT_USER_SESSION_INFO.value)
        parent.register_handler(char_handlers.Plugin.handle_minifigure_creation,
                                packet_enum.PacketHeader.CLIENT_MINIFIGURE_CREATE_REQUEST.value)
        parent.register_handler(char_handlers.Plugin.handle_load_world,
                                packet_enum.PacketHeader.CLIENT_ENTER_WORLD.value)
        parent.register_handler(char_handlers.Plugin.handle_minifigure_delete,
                                packet_enum.PacketHeader.CLIENT_DELETE_MINIFIGURE_REQUEST.value)
        print("Registered Needed Character Handling")
        parent.register_handler(Plugin.handle_handshake, packet_enum.PacketHeader.HANDSHAKE.value)
        parent.register_handler(Plugin.handle_detailed_user_info,
                                packet_enum.PacketHeader.CLIENT_LOAD_COMPLETE.value)

    @classmethod
    def handle_handshake(cls, data: bytes, address, server):
        """
        Handles initial connection between server and client.
        """
        player = server.lookup_player_by_ip(address[0])
        c = server.db_connection.cursor()
        c.execute("SELECT position FROM wlus.character_info WHERE player_id = %s", (int(player["id"]),))
        player_pos = c.fetchone()[0]
        if player_pos == "0,0,0":
            world_info = world_to_client.WorldInfoPacket.from_cdclient(server.zone, default_spawn=True)
            c.execute("UPDATE wlus.character_info SET position = %s WHERE player_id = %s",
                      (str(world_info.player_position), int(player["id"])))
            server.db_connection.commit()
        else:
            world_info = world_to_client.WorldInfoPacket.from_cdclient(server.zone, default_spawn=False)
            points = player_pos.split(",")
            pos = misc_serializables.Vector3()
            pos.x = float(points[0])
            pos.y = float(points[1])
            pos.z = float(points[2])
            world_info.player_position = pos
        packet = WriteStream()
        packet.write(packet_enum.PacketHeader.WORLD_INFO.value)
        packet.write(world_info)
        server.send(packet, address)

    @classmethod
    def handle_detailed_user_info(cls, data: bytes, address, server):
        print("Client Load Complete")

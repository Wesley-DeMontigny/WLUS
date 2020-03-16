"""
This will handle all of the character related packets.
"""
from ..serializables import packet_enum, world_to_client, client_to_world, global_packets, misc_serializables
from pyraknet.bitstream import *
import os


class Plugin:
    def __init__(self, parent):
        print("Character Handler Initiated")
        parent.register_handler(Plugin.handle_handshake, packet_enum.PacketHeader.HANDSHAKE.value)
        parent.register_handler(Plugin.handle_minifigure_list_request,
                                packet_enum.PacketHeader.CLIENT_USER_SESSION_INFO.value)
        parent.register_handler(Plugin.handle_minifigure_creation,
                                packet_enum.PacketHeader.CLIENT_MINIFIGURE_CREATE_REQUEST.value)
        parent.register_handler(Plugin.handle_load_world,
                                packet_enum.PacketHeader.CLIENT_ENTER_WORLD.value)
        parent.register_handler(Plugin.handle_minifigure_delete,
                                packet_enum.PacketHeader.CLIENT_DELETE_MINIFIGURE_REQUEST.value)

    @classmethod
    def handle_handshake(cls, data: bytes, address, server):
        """
        Handles initial connection between server and client.
        Changes current instance of the session
        """
        stream = ReadStream(data)
        client_handshake = stream.read(global_packets.HandshakePacket)
        print(f"{address[0]} has initiated handshake - Client has version {client_handshake.game_version}")

        server_handshake = global_packets.HandshakePacket()
        server_handshake.remote_connection_type = 4
        packet = WriteStream()
        packet.write(packet_enum.PacketHeader.HANDSHAKE.value)
        packet.write(server_handshake)
        server.send(packet, address)

    @classmethod
    def handle_load_world(cls, data: bytes, address, server):
        """
        Handles when the user hits the play button.
        """
        stream = ReadStream(data)
        player_id = stream.read(client_to_world.JoinWorldPacket).object_id
        c = server.db_connection.cursor()
        c.execute("SELECT zone, current_name FROM wlus.character WHERE character_id = %s", (player_id,))
        char_data = c.fetchone()
        session = server.lookup_session_by_ip(address[0])
        zone_id = char_data[0]
        if zone_id == 0:
            zone_id = 1000

        player = server.lookup_player_by_ip(address[0])
        if player is None:
            server.execute_master_query("""INSERT INTO online_players(id, session_id, current_zone, name)
            VALUES (%s, %s, %s, "%s")""" % (player_id, session["id"], zone_id, char_data[1]), do_return=False)
        else:
            server.execute_master_query("""UPDATE online_players SET id = %s, zone_id = %s, name = "%s"
             WHERE session_id = %s""" % (player_id, zone_id, char_data[1], player["session_id"]), do_return=False)

        if zone_id != server.zone:
            ip_address, port, instance_name = server.redirect_request("zone", str(zone_id))
            print(f"Redirecting {address} to instance {instance_name}, which is at {ip_address, port}")
            redirect_packet = world_to_client.RedirectiontoNewServerPacket()
            redirect_packet.redirect_port = int(port)
            redirect_packet.redirect_ip = ip_address
            packet = WriteStream()
            packet.write(packet_enum.PacketHeader.REDIRECT_TO_NEW_SERVER.value)
            packet.write(redirect_packet)
            server.update_session_instance(instance=instance_name, ip_address=address[0])
            server.send(packet, address)
        else:
            c.execute("SELECT position FROM wlus.character_info WHERE player_id = %s", (player_id,))
            player_pos = c.fetchone()[0]
            if player_pos == "0,0,0":
                world_info = world_to_client.WorldInfoPacket.from_cdclient(zone_id, default_spawn=True)
                c.execute("UPDATE wlus.character_info SET position = %s WHERE player_id = %s",
                          (str(world_info.player_position), player_id))
                server.db_connection.commit()
            else:
                world_info = world_to_client.WorldInfoPacket.from_cdclient(zone_id, default_spawn=False)
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
    def handle_minifigure_delete(cls, data: bytes, address, server):
        """
        Handles when the user deletes a minifigure.s
        """
        stream = ReadStream(data)
        character_id = stream.read(client_to_world.CharacterDeleteRequestPacket).object_id
        c = server.db_connection.cursor()
        session = server.lookup_session_by_ip(address[0])
        c.execute("SELECT account_id FROM wlus.account WHERE username = %s", (session["username"],))
        account_id = c.fetchone()[0]
        c.execute("SELECT * FROM wlus.character WHERE account_id = %s AND character_id = %s",
                  (account_id, int(character_id)))
        data = c.fetchone()
        if data:
            c.execute("DELETE FROM wlus.character WHERE account_id = %s AND character_id = %s",
                      (account_id, int(character_id)))
            c.execute("DELETE FROM wlus.inventory WHERE player_id = %s", (int(character_id),))
            c.execute("DELETE FROM wlus.character_stats WHERE player_id = %s", (int(character_id),))
            c.execute("DELETE FROM wlus.character_info WHERE player_id = %s", (int(character_id),))
            server.db_connection.commit()

    @classmethod
    def handle_minifigure_creation(cls, data: bytes, address, server):
        c = server.db_connection.cursor()
        session = server.lookup_session_by_ip(address[0])
        c.execute("SELECT account_id FROM wlus.account WHERE username = %s", (session["username"],))
        account_id = c.fetchone()[0]

        stream = ReadStream(data)
        minfig = stream.read(client_to_world.MinifigureCreateRequestPacket).to_login_character()
        minfig.save_to_db(account_id, server.db_connection)

        response = world_to_client.MinifigureCreationResponsePacket()
        response.response = 0x00
        packet = WriteStream()
        packet.write(packet_enum.PacketHeader.MINIFIGURE_CREATION_RESPONSE.value)
        packet.write(response)
        server.send(packet, address)

        characters = []
        c.execute("SELECT * FROM wlus.character WHERE account_id = %s", (account_id,))
        minifig_results = c.fetchall()
        for minifig in minifig_results:
            char = misc_serializables.LoginCharacter()
            char.object_id = minifig[0]
            char.current_name = minifig[1]
            char.unapproved_name = minifig[2]
            char.head_color = minifig[3]
            char.head = minifig[4]
            char.chest_color = minifig[5]
            char.chest = minifig[6]
            char.legs = minifig[7]
            char.hair_style = minifig[8]
            char.hair_color = minifig[9]
            char.left_hand = minifig[10]
            char.right_hand = minifig[11]
            char.eyebrows_style = minifig[12]
            char.eyes_style = minifig[13]
            char.mouth_style = minifig[14]
            char.last_zone = minfig[16]
            c.execute("SELECT * FROM wlus.inventory WHERE player_id = %s AND equipped = 1", (char.object_id,))
            equipped_items = c.fetchall()
            for i in equipped_items:
                char.equipped_items.append(i[1])
            characters.append(char)

        char_list = world_to_client.MinfigureListPacket()
        for c in characters:
            char_list.minifigs.append(c)
        packet = WriteStream()
        packet.write(packet_enum.PacketHeader.MINIFIGURE_LIST.value)
        packet.write(char_list)
        server.send(packet, address)

    @classmethod
    def handle_minifigure_list_request(cls, data: bytes, address, server):
        stream = ReadStream(data)
        session_info = stream.read(client_to_world.UserSessionInfoPacket)
        c = server.db_connection.cursor()
        session = server.lookup_session_by_username(session_info.username)
        if session:
            if session["user_key"] == session_info.user_key:
                packet = WriteStream()

                c.execute("SELECT account_id FROM account WHERE username = %s", (session_info.username,))
                account_id = c.fetchone()[0]

                characters = []
                c.execute("SELECT * FROM wlus.character WHERE account_id = %s", (account_id,))
                minifig_results = c.fetchall()
                for minifig in minifig_results:
                    char = misc_serializables.LoginCharacter()
                    char.object_id = minifig[0]
                    char.current_name = minifig[1]
                    char.unapproved_name = minifig[2]
                    char.head_color = minifig[3]
                    char.head = minifig[4]
                    char.chest_color = minifig[5]
                    char.chest = minifig[6]
                    char.legs = minifig[7]
                    char.hair_style = minifig[8]
                    char.hair_color = minifig[9]
                    char.left_hand = minifig[10]
                    char.right_hand = minifig[11]
                    char.eyebrows_style = minifig[12]
                    char.eyes_style = minifig[13]
                    char.mouth_style = minifig[14]
                    c.execute("SELECT * FROM wlus.inventory WHERE player_id = %s AND equipped = 1", (char.object_id,))
                    equipped_items = c.fetchall()
                    for i in equipped_items:
                        char.equipped_items.append(i[1])
                    characters.append(char)

                char_list = world_to_client.MinfigureListPacket()
                for c in characters:
                    char_list.minifigs.append(c)

                packet.write(packet_enum.PacketHeader.MINIFIGURE_LIST.value)
                packet.write(char_list)
                server.send(packet, address)
            else:
                disconnect = global_packets.DisconnectNotifyPacket()
                disconnect.disconnect_id = packet_enum.DisconnectionNotify.INVALID_SESSION_KEY.value
                disconnect.send(server, address)
        else:
            disconnect = global_packets.DisconnectNotifyPacket()
            disconnect.disconnect_id = packet_enum.DisconnectionNotify.INVALID_SESSION_KEY.value
            disconnect.send(server, address)

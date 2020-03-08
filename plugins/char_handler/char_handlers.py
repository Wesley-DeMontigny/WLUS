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

    @classmethod
    def handle_handshake(cls, data: bytes, address, server):
        """
        Handles initial connection between server and client.
        """
        stream = ReadStream(data)
        client_handshake = stream.read(global_packets.HandshakePacket)
        print(f"{address[0]} has initiated handshake - Client has version {client_handshake.game_version}")

        server_handshake = global_packets.HandshakePacket()
        server_handshake.remote_connection_type = 4
        server_handshake.process_id = os.getpid()
        packet = WriteStream()
        packet.write(packet_enum.PacketHeader.HANDSHAKE.value)
        packet.write(server_handshake)
        server.send(packet, address)

    @classmethod
    def handle_minifigure_creation(cls, data: bytes, address, server):
        c = server.db_connection.cursor()
        c.execute("SELECT * FROM wlus.session WHERE ip_address = %s", (str(address),))
        session = c.fetchone()
        c.execute("SELECT account_id FROM wlus.account WHERE username = %s", (session[1],))
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
        c.execute("SELECT * FROM wlus.session WHERE username = %s", (session_info.username,))
        results = c.fetchall()
        if results is not None:
            sessions = [dict(zip(c.column_names, result)) for result in results]
            if sessions[0]["user_key"] == session_info.user_key:
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

                """
                # Add Duke Exeter (For Testing)
                exeter = misc_serializables.LoginCharacter.from_cdclient(12261)
                exeter.equipped_items.append(7369)
                exeter.equipped_items.append(7381)
                char_list.minifigs.append(exeter)
                """

                packet.write(packet_enum.PacketHeader.MINIFIGURE_LIST.value)
                packet.write(char_list)
                server.send(packet, address)
            else:
                disconnect = global_packets.DisconnectNotifyPacket()
                disconnect.disconnect_id = packet_enum.DisconnectionNotify.INVALID_SESSION_KEY.value
                disconnect_packet = WriteStream()
                disconnect_packet.write(packet_enum.PacketHeader.DISCONNECT_NOTIFY.value)
                disconnect_packet.write(disconnect)
                server.send(disconnect_packet, address)
        else:
            disconnect = global_packets.DisconnectNotifyPacket()
            disconnect.disconnect_id = packet_enum.DisconnectionNotify.INVALID_SESSION_KEY.value
            disconnect_packet = WriteStream()
            disconnect_packet.write(packet_enum.PacketHeader.DISCONNECT_NOTIFY.value)
            disconnect_packet.write(disconnect)
            server.send(disconnect_packet, address)

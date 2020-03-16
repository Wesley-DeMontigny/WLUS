"""
This will handle all of the character related packets.
"""
from ..serializables import packet_enum, world_to_client, client_to_world, global_packets, misc_serializables, replica_components
from pyraknet.bitstream import *
from pyraknet.replicamanager import *
from pyraknet.messages import Message
from ..char_handler import char_handlers
from xml.etree import ElementTree


class Plugin:
    def __init__(self, parent):
        print("World Handler Initiated")
        parent.register_handler(Plugin.handle_minifigure_list_request,
                                packet_enum.PacketHeader.CLIENT_MINIFIGURE_LIST_REQUEST.value)
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
        parent.register_handler(Plugin.handle_sesion_info, packet_enum.PacketHeader.CLIENT_USER_SESSION_INFO.value)

        parent.additional_config["replica_manager"] = ReplicaManager(parent)

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
        packet = WriteStream()
        packet.write(packet_enum.PacketHeader.HANDSHAKE.value)
        packet.write(server_handshake)
        server.send(packet, address)

    @classmethod
    def handle_sesion_info(cls, data: bytes, address, server):
        stream = ReadStream(data)
        session_info = stream.read(client_to_world.UserSessionInfoPacket)
        c = server.db_connection.cursor()
        session = server.lookup_session_by_username(session_info.username)

        if session is not None:
            if session["user_key"] == session_info.user_key:
                # Add user to replica manager
                server.additional_config["replica_manager"].add_participant(address)

                # Send world info packet if the session key is correct
                player = server.lookup_player_by_ip(address[0])
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

            else:
                disconnect = global_packets.DisconnectNotifyPacket()
                disconnect.disconnect_id = packet_enum.DisconnectionNotify.INVALID_SESSION_KEY.value
                disconnect.send(server, address)
        else:
            disconnect = global_packets.DisconnectNotifyPacket()
            disconnect.disconnect_id = packet_enum.DisconnectionNotify.INVALID_SESSION_KEY.value
            disconnect.send(server, address)

    @classmethod
    def handle_detailed_user_info(cls, data: bytes, address, server):
        # I'm honestly just going to ignore what the client sends here. I don't need to do anything with it
        print(f"Sending detailed user info to {address}")
        player_info = server.lookup_player_by_ip(address[0])
        c = server.db_connection.cursor()
        c.execute("SELECT backpack_space, currency, universe_score, level, position, rotation, health,"
                  " max_health, armor, max_armor, imagination, max_imagination FROM character_info WHERE player_id = %s"
                  , (player_info["id"],))
        character_info = c.fetchone()
        c.execute("SELECT * FROM wlus.inventory WHERE player_id = %s", (player_info["id"],))
        inventory = c.fetchall()
        c.execute("SELECT mission_id FROM wlus.completed_missions WHERE player_id = %s", (player_info["id"],))
        complete_missions = c.fetchall()
        c.execute("SELECT mission_id, progress FROM wlus.current_missions WHERE player_id = %s", (player_info["id"],))
        current_missions = c.fetchall()

        dui = world_to_client.DetailedUserInfoPacket()
        dui.ldf.register_key("levelid", int(player_info["current_zone"]), 1)
        dui.ldf.register_key("objid", int(player_info["id"]), 9)
        dui.ldf.register_key("template", 1, 1)
        dui.ldf.register_key("name", player_info["name"], 0)

        root = ElementTree.Element("obj")
        root.set("v", "1")
        buff = ElementTree.SubElement(root, "buff")
        skill = ElementTree.SubElement(root, "skill")

        inv = ElementTree.SubElement(root, "inv")
        bag = ElementTree.SubElement(inv, "bag")
        bag_info = ElementTree.SubElement(bag, "b")
        bag_info.set("t", "0")
        bag_info.set("m", str(character_info[0]))
        items = ElementTree.SubElement(inv, "items")
        item_in = ElementTree.SubElement(items, "in")
        for item in inventory:
            i = ElementTree.SubElement(item_in, "i")
            i.set("l", str(item[1]))
            i.set("id", str(item[0]))
            i.set("s", str(item[2]))
            i.set("c", str(item[5]))
            i.set("b", str(item[4]))
            i.set("eq", str(item[3]))

        mf = ElementTree.SubElement(root, "mf")
        char = ElementTree.SubElement(root, "char")
        char.set("cc", str(character_info[1]))
        char.set("ls", str(character_info[2]))
        lvl = ElementTree.SubElement(root, "lvl")
        lvl.set("l", str(character_info[3]))

        pets = ElementTree.SubElement(root, "pet")

        mis = ElementTree.SubElement(root, "mis")
        done = ElementTree.SubElement(mis, "done")
        for mission in complete_missions:
            m = ElementTree.SubElement(done, "m")
            m.set("id", str(mission[0]))
            m.set("cct", "1")
            m.set("cts", "0")
        cur = ElementTree.SubElement(mis, "cur")
        for mission in current_missions:
            m = ElementTree.SubElement(cur, "m")
            m.set("id", str(mission[0]))
            sv = ElementTree.SubElement(m, "sv")
            sv.set("v", str(mission[1]))

        dui.ldf.register_key("xmlData", root, 13)

        packet = WriteStream()
        packet.write(packet_enum.PacketHeader.DETAILED_USER_INFO.value)
        packet.write(dui)
        server.send(packet, address)

        c.execute("SELECT * FROM character_stats WHERE player_id = %s", (player_info["id"],))
        character_stats = c.fetchone()
        c.execute("SELECT * FROM wlus.character WHERE character_id = %s", (player_info["id"],))
        character_data = c.fetchone()

        player = replica_components.ReplicaObject()
        player.base_data.lot = 1
        player.base_data.object_id = int(player_info["id"])
        player.base_data.name = player_info["name"]

        player.components[packet_enum.SerializedComponents.COMPONENT_107.value] = replica_components.Component107()

        player.components[packet_enum.SerializedComponents.RENDER.value] = replica_components.RenderComponent()

        player.components[packet_enum.SerializedComponents.SKILL.value] = replica_components.SkillComponent()

        inventory_comp = replica_components.InventoryComponent()
        for item in inventory:
            inventory_item = replica_components.InventoryItem()
            inventory_item.lot = item[1]
            inventory_item.slot = item[2]
            inventory_item.count = item[5]
            inventory_item.object_id = item[0]
            inventory_comp.items.append(inventory_item)
        player.components[packet_enum.SerializedComponents.INVENTORY.value] = inventory_comp

        controllable_physics = replica_components.ControllablePhysicsComponent()
        pos = misc_serializables.Vector3()
        p_points = character_info[4].split(",")
        pos.x = float(p_points[0])
        pos.y = float(p_points[1])
        pos.z = float(p_points[2])
        controllable_physics.position = pos
        rot = misc_serializables.Vector4()
        r_points = character_info[5].split(",")
        rot.x = float(r_points[0])
        rot.y = float(r_points[1])
        rot.z = float(r_points[2])
        rot.w = float(r_points[3])
        controllable_physics.rotation = rot
        player.components[packet_enum.SerializedComponents.CONTROLLABLE_PHYSICS.value] = controllable_physics

        destructible_component = replica_components.DestructibleComponent()
        stats_index = replica_components.StatsIndex()
        stats_index.factions.append(1)
        stats_index.health = character_info[6]
        stats_index.max_health = character_info[7]
        stats_index.armor = character_info[8]
        stats_index.max_armor = character_info[9]
        stats_index.imagination = character_info[10]
        stats_index.max_imagination = character_info[11]
        destructible_component.stats_index = stats_index
        destructible_component.destructible_index = replica_components.DestructibleIndex()
        player.components[packet_enum.SerializedComponents.DESTRUCTIBLE.value] = destructible_component

        character_component = replica_components.CharacterComponent()
        character_component.character_stats = character_stats[1:]
        character_component.lego_score = character_info[2]
        character_component.shirt_color = character_data[5]
        character_component.pants_color = character_data[7]
        character_component.hair_style = character_data[8]
        character_component.hair_color = character_data[9]
        character_component.eyebrows = character_data[12]
        character_component.eyes = character_data[13]
        character_component.mouth = character_data[14]
        character_component.account_id = character_data[15]
        character_component.activity = 1
        player.components[packet_enum.SerializedComponents.CHARACTER.value] = character_component

        server.additional_config["replica_manager"].construct(player)

        server_done = WriteStream()
        server_done.write(packet_enum.PacketHeader.SERVER_GAME_MESSAGE.value)
        server_done.write(c_int64(int(player_info["id"])))
        server_done.write(c_uint16(packet_enum.GameMessages.SERVER_DONE_LOADING_OBJECTS.value))
        server.send(server_done, address)

        player_ready = WriteStream()
        player_ready.write(packet_enum.PacketHeader.SERVER_GAME_MESSAGE.value)
        player_ready.write(c_int64(int(player_info["id"])))
        player_ready.write(c_uint16(packet_enum.GameMessages.PLAYER_READY.value))
        server.send(player_ready, address)

    # This is just slightly different from the character instance handler
    @classmethod
    def handle_minifigure_list_request(cls, data: bytes, address, server):
        c = server.db_connection.cursor()
        packet = WriteStream()
        session = server.lookup_session_by_ip(address[0])
        c.execute("SELECT account_id FROM account WHERE username = %s", (session["username"],))
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

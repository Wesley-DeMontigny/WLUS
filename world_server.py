import pyraknet.server
import pyraknet.messages
import time
import game_enums
import os
import game_types
from pyraknet.bitstream import *
import zlib
from xml.etree import ElementTree


class WorldServer(pyraknet.server.Server):
	def __init__(self, address: pyraknet.messages.Address, max_connections: int, incoming_password: bytes, world_server_service):
		super().__init__(address, max_connections, incoming_password)
		self._world_server_service = world_server_service
		self.add_handler(pyraknet.server.Event.UserPacket, self.handle_packet)
		self._userpacket_handlers = {}
		global game
		game = self._world_server_service.get_parent()
		self.default_handlers = {"world_handshake":["OnPacket_World_{}".format(game_enums.PacketHeaderEnum.HANDSHAKE.value), self.handle_handshake],
								 "world_session_info":["OnPacket_World_{}".format(game_enums.PacketHeaderEnum.CLIENT_USER_SESSION_INFO.value), self.handle_session_info],
								 "world_minifigure_list":["OnPacket_World_{}".format(game_enums.PacketHeaderEnum.CLIENT_MINIFIGURE_LIST_REQUEST.value), self.handle_minifig_list_request],
								 "world_minifig_creation":["OnPacket_World_{}".format(game_enums.PacketHeaderEnum.CLIENT_MINIFIGURE_CREATE_REQUEST.value), self.handle_minifig_creation],
								 "world_minifig_deletion:":["OnPacket_World_{}".format(game_enums.PacketHeaderEnum.CLIENT_DELETE_MINIFIGURE_REQUEST.value), self.handle_minifig_deletion],
								 "world_join_world":["OnPacket_World_{}".format(game_enums.PacketHeaderEnum.CLINET_ENTER_WORLD.value), self.handle_join_world],
								 "world_detailed_user_info":["OnPacket_World_{}".format(game_enums.PacketHeaderEnum.CLIENT_LOAD_COMPLETE.value), self.handle_detailed_user_info]}

	def handle_handshake(self, data: bytes, address):
		stream = ReadStream(data)
		client_version = stream.read(c_ulong)

		packet = WriteStream()
		packet.write(game_enums.PacketHeaderEnum.HANDSHAKE.value)
		packet.write(c_ulong(client_version))
		packet.write(c_ulong(0x93))
		packet.write(c_ulong(4))  # Connection Type (1 For Auth, 4 For Everything Else)
		packet.write(c_ulong(os.getpid()))
		packet.write(c_short(0xff))  # Local port
		packet.write(game.get_config("address"), allocated_length=33)

		self.send(packet, address)

	def handle_minifig_creation(self, data: bytes, address):
		stream = ReadStream(data)
		custom_name = stream.read(str, allocated_length=33)

		firstname_file = open("./resources/minifigname_first.txt", 'r')
		firstnames = firstname_file.readlines()
		firstname_file.close()

		middlename_file = open("./resources/minifigname_middle.txt", 'r')
		middlenames = middlename_file.readlines()
		middlename_file.close()

		lastname_file = open("./resources/minifigname_last.txt", 'r')
		lastnames = lastname_file.readlines()
		lastname_file.close()

		predef_name1 = firstnames[stream.read(c_ulong)]
		predef_name2 = middlenames[stream.read(c_ulong)]
		predef_name3 = lastnames[stream.read(c_ulong)]

		stream.read(bytes, allocated_length=9)
		shirt_color = stream.read(c_ulong)
		shirt_style = stream.read(c_ulong)
		pants_color = stream.read(c_ulong)
		hair_style = stream.read(c_ulong)
		hair_color = stream.read(c_ulong)
		lh = stream.read(c_ulong)
		rh = stream.read(c_ulong)
		eyebrows = stream.read(c_ulong)
		eyes = stream.read(c_ulong)
		mouth = stream.read(c_ulong)

		player_service = game.get_service("Player")
		session_service = game.get_service("Session")
		session = session_service.get_session_by_address(address)
		if(custom_name == "" or game.get_config("accept_custom_names") == False):
			name = str(predef_name1 + predef_name2 + predef_name3).rstrip('\n')
		else:
			name = custom_name
		player_service.create_player(session.account_id, name, shirt_color, shirt_style, pants_color, hair_color, hair_style, lh, rh, eyebrows, eyes, mouth, custom_name)

		packet = WriteStream()
		packet.write(game_enums.PacketHeaderEnum.MINIFIGURE_CREATION_RESPONSE.value)
		packet.write(c_uint8(game_enums.MinifigureCreationResponseEnum.SUCCESS))
		self.send(packet, address)

		time.sleep(.5)
		self.handle_minifig_list_request(data, address)

	def load_world(self, player_id: int, level_id: int, address, spawn_at_default: bool = False):
		packet = WriteStream()
		player = game.get_service("Player").get_player_by_id(player_id)
		world = game.get_service("World")
		session = game.get_service("Session").get_session_by_address(address)
		session.player_id = player_id
		scene = world.get_scenes_by_level(level_id)[0]
		print("Sending Player {} to {}".format(player_id, scene.get_name()))
		packet.write(game_enums.PacketHeaderEnum.WORLD_INFO.value)

		packet.write(c_uint16(level_id))
		packet.write(c_uint16(0))  # Map Instance
		packet.write(c_ulong(0))  # Map Clone
		packet.write(c_ulong(game_enums.zone_checksums[level_id]))
		if (spawn_at_default):
			packet.write(c_float(game_enums.default_zone_spawns[level_id][0]))
			packet.write(c_float(game_enums.default_zone_spawns[level_id][1]))
			packet.write(c_float(game_enums.default_zone_spawns[level_id][2]))
			player["position"] = game_types.Vector3(game_enums.default_zone_spawns[level_id][0], game_enums.default_zone_spawns[level_id][1], game_enums.default_zone_spawns[level_id][2])
		else:
			packet.write(c_float(player["position"].X))
			packet.write(c_float(player["position"].Y))
			packet.write(c_float(player["position"].Z))
		if (scene.is_activity()):
			packet.write(c_ulong(4))
		else:
			packet.write(c_ulong(0))
		if(session.scene_id == 0):
			scene.add_player(player_id)
		else:
			game.get_pyobject(session.scene_id).remove_player(player_id)
			scene.add_player(player_id)
		session.scene_id = scene.get_py_id()
		self.send(packet, session.address)
		game.trigger_event("LoadWorld", args=[player_id, level_id])

	def handle_detailed_user_info(self, data: bytes, address):
		session = game.get_service("Session").get_session_by_address(address)
		player = game.get_service("Player").get_player_by_id(session.player_id)

		ldf = game_types.LDF()
		ldf.register_key("levelid", player["zone"], 1)
		ldf.register_key("objid", player["player_id"], 9)
		ldf.register_key("template", 1, 1)
		ldf.register_key("name", player["name"], 0)

		root = ElementTree.Element("obj")
		root.set("v", "1")
		buff = ElementTree.SubElement(root, "buff")
		skill = ElementTree.SubElement(root, "skill")

		inv = ElementTree.SubElement(root, "inv")
		bag = ElementTree.SubElement(inv, "bag")
		bag_info = ElementTree.SubElement(bag, "b")
		bag_info.set("t", "0")
		bag_info.set("m", str(player["Data"]["backpack_space"]))
		items = ElementTree.SubElement(inv, "items")
		item_in = ElementTree.SubElement(items, "in")
		for item in player["Inventory"]:
			i = ElementTree.SubElement(item_in, "i")
			i.set("l", str(item["lot"]))
			i.set("id", str(item["item_id"]))
			i.set("s", str(item["lot"]))
			i.set("c", str(item["quantity"]))
			i.set("b", str(int(item["linked"])))
			i.set("eq", str(int(item["equipped"])))

		mf = ElementTree.SubElement(root, "mf")
		char = ElementTree.SubElement(root, "char")
		char.set("cc", str(player["currency"]))
		char.set("ls", str(player["universe_score"]))
		lvl = ElementTree.SubElement(root, "lvl")
		lvl.set("l", str(player["level"]))

		pets = ElementTree.SubElement(root, "pet")

		mis = ElementTree.SubElement(root, "mis")
		done = ElementTree.SubElement(mis, "done")
		for mission in player["CompletedMissions"]:
			m = ElementTree.SubElement(done, "m")
			m.set("id", str(mission["mission_id"]))
			m.set("cct", "1")
			m.set("cts", "0")
		cur = ElementTree.SubElement(mis, "cur")
		for mission in player["CurrentMissions"]:
			m = ElementTree.SubElement(cur, "m")
			m.set("id", str(mission["mission_id"]))
			sv = ElementTree.SubElement(m, "sv")
			sv.set("v", str(mission["progress"]))

		ldf.register_key("xmlData", root, 13)

		lego_data = WriteStream()
		ldf.write_to_stream(lego_data)
		ldf_bytes = bytes(lego_data)
		compressed = zlib.compress(ldf_bytes)

		packet = WriteStream()
		packet.write(game_enums.PacketHeaderEnum.DETAILED_USER_INFO)
		packet.write(c_ulong(len(compressed) + 9))
		packet.write(c_bool(True))
		packet.write(c_ulong(len(ldf_bytes)))
		packet.write(c_ulong(len(compressed)))
		packet.write(compressed)

		self.send(packet, address)
		print("Sent Detailed User Info To {}".format(player["name"]))

	def handle_join_world(self, data: bytes, address):
		stream = ReadStream(data)
		player_id = stream.read(c_longlong)
		player = game.get_service("Player").get_player_by_id(player_id)
		if (player["zone"] == 0):
			player["zone"] = 1000
		spawn_at_default = False
		if (player["Data"]["position"].X < 2 and player["Data"]["position"].Y < 2 and player["Data"]["position"].Z < 2):
			spawn_at_default = True
		self.load_world(player_id, player["zone"], address, spawn_at_default=spawn_at_default)

	def handle_session_info(self, data: bytes, address):
		stream = ReadStream(data)
		username = stream.read(str, allocated_length=33)
		user_key = stream.read(str, allocated_length=33)

		session = game.get_service("Session").get_session_by_address(address)
		if(session is not None):
			if (session.user_key == user_key and session.username == username):
				print(address, "Sent The Following Valid Key:", user_key)
			else:
				print(address, "Sent The Following Invalid Key:", user_key)
				disconnect_packet = WriteStream()
				disconnect_packet.write(game_enums.PacketHeaderEnum.DISCONNECT_NOTIFY.value)
				disconnect_packet.write(c_ulong(game_enums.DisconnectionReasonEnum.INVALID_SESSION_KEY))
				self.send(disconnect_packet, address)
		else:
			print("Unknown Session!")
			disconnect_packet = WriteStream()
			disconnect_packet.write(game_enums.PacketHeaderEnum.DISCONNECT_NOTIFY.value)
			disconnect_packet.write(c_ulong(game_enums.DisconnectionReasonEnum.UNKNOWN_ERROR))
			self.send(disconnect_packet, address)

	def handle_minifig_list_request(self, data : bytes, address):
		time.sleep(1)
		session = game.get_service("Session").get_session_by_address(address)
		player_service = game.get_service("Player")
		account = player_service.get_account_by_id(session.account_id)
		characters = account["Characters"]
		packet = WriteStream()
		packet.write(game_enums.PacketHeaderEnum.MINIFIGURE_LIST.value)
		packet.write(c_uint8(len(characters)))
		packet.write(c_uint8(0))
		for character in characters:
			packet.write(c_longlong(character["player_id"]))  # Object ID
			packet.write(c_ulong(0))
			packet.write(character["name"], allocated_length=33)  # Character Name
			if(character["custom_name"] != ""):
				packet.write(character["custom_name"], allocated_length=33)  # Custom Name
			else:
				packet.write("", allocated_length=33)
			packet.write(c_bool(False))  # Name rejected
			packet.write(c_bool(False))  # Free to play
			packet.write(game_types.String("", allocated_length=10))
			packet.write(c_ulong(character["shirt_color"]))
			packet.write(c_ulong(character["shirt_style"]))
			packet.write(c_ulong(character["pants_color"]))
			packet.write(c_ulong(character["hair_style"]))
			packet.write(c_ulong(character["hair_color"]))
			packet.write(c_ulong(character["lh"]))
			packet.write(c_ulong(character["rh"]))
			packet.write(c_ulong(character["eyebrows"]))
			packet.write(c_ulong(character["eyes"]))
			packet.write(c_ulong(character["mouth"]))
			packet.write(c_ulong(0))
			packet.write(c_uint16(character["zone"]))
			packet.write(c_uint16(0))  # MapInstance
			packet.write(c_ulong(0))  # MapClone
			packet.write(c_ulonglong(0))
			equippedItems = player_service.get_equipped_items(character["player_id"])
			packet.write(c_ushort(len(equippedItems)))
			for item in equippedItems:
				packet.write(c_ulong(item["lot"]))
		try:
			self.send(packet, address)
		except:
			pass

	def handle_minifig_deletion(self, data: bytes, address):
		stream = ReadStream(data)
		player_id = stream.read(c_longlong)
		game.get_service("Player").delete_player(player_id)


	def handle_packet(self, data : bytes, address : pyraknet.messages.Address):
		game.trigger_event("OnPacket_World_{}".format(str(data[0:8])), args=[data[8:], address], debug=True)
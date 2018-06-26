import pyraknet.server
import pyraknet.messages
import time
import game_enums
import os
import game_types
from pyraknet.bitstream import *


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
								 "world_minifig_creation":["OnPacket_World_{}".format(game_enums.PacketHeaderEnum.CLIENT_MINIFIGURE_CREATE_REQUEST.value), self.handle_minifig_creation]}

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
		name = stream.read(str, allocated_length=33)
		predef_name1 = stream.read(c_ulong)
		predef_name2 = stream.read(c_ulong)
		predef_name3 = stream.read(c_ulong)
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
		player_service.create_player(session.account_id, name, shirt_color, shirt_style, pants_color, hair_color, hair_style, lh, rh, eyebrows, eyes, mouth)

		packet = WriteStream()
		packet.write(game_enums.PacketHeaderEnum.MINIFIGURE_CREATION_RESPONSE)
		packet.write(c_uint8(game_enums.MinifigureCreationResponseEnum.SUCCESS))
		self.send(packet, address)

		time.sleep(.5)
		self.handle_minifig_list_request(data, address)

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
			packet.write("", allocated_length=33)  # Name to show up in paranthesis
			packet.write(c_bool(False))  # Name rejected
			packet.write(c_bool(False))  # Free to play
			packet.write(game_types.String("", allocated_length=10))  # Unknown
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


	def handle_packet(self, data : bytes, address : pyraknet.messages.Address):
		game.trigger_event("OnPacket_World_{}".format(str(data[0:8])), args=[data[8:], address])
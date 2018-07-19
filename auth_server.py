import pyraknet.server
import pyraknet.messages
import typing
import threading
import uuid
import game_types
from pyraknet.bitstream import *
import game_enums
import os


class AuthServer(pyraknet.server.Server):
	def __init__(self, address: pyraknet.messages.Address, max_connections: int, incoming_password: bytes, auth_server_service):
		super().__init__(address, max_connections, incoming_password)
		self.auth_server_service = auth_server_service
		self.add_handler(pyraknet.server.Event.UserPacket, self.handle_packet)
		global game
		game = self.auth_server_service.get_parent()
		self.default_handlers = {"auth_handshake":["OnPacket_Auth_{}".format(game_enums.PacketHeaderEnum.HANDSHAKE.value), self.handle_handshake],
								 "auth_login":["OnPacket_Auth_{}".format(game_enums.PacketHeaderEnum.CLIENT_LOGIN_INFO.value), self.handle_login]}


	def handle_handshake(self, data: bytes, address):
		stream = ReadStream(data)
		client_version = stream.read(c_ulong)

		packet = WriteStream()
		packet.write(game_enums.PacketHeaderEnum.HANDSHAKE.value)
		packet.write(c_ulong(client_version))
		packet.write(c_ulong(0x93))
		packet.write(c_ulong(1))  # Connection Type (1 For Auth, 4 For Everything Else)
		packet.write(c_ulong(os.getpid()))
		packet.write(c_short(0xff))  # Local port
		packet.write(game.get_config("redirect_address"), allocated_length=33)

		self.send(packet, address)

	def handle_login(self, data: bytes, address):
		stream = ReadStream(data)
		username = stream.read(str, allocated_length=33)
		password = stream.read(str, allocated_length=41)

		packet = WriteStream()
		print("Attempted Login With Username '{}' And Password '{}'".format(username, password))
		login, user_info = self.auth_server_service.validate_login(username, password)
		if (login):
			response = game_enums.LoginResponseEnum.SUCCESS.value
			print("Login Accepted!")
		else:
			response = game_enums.LoginResponseEnum.INVALID_LOGIN_INFO.value
			print("Login Rejected!")
		packet.write(game_enums.PacketHeaderEnum.LOGIN_RESPONSE.value)
		packet.write(c_uint8(response))
		packet.write(game_types.String("Talk_Like_A_Pirate", allocated_length=33))
		packet.write(game_types.String("", allocated_length=33 * 7))
		packet.write(c_ushort(1))
		packet.write(c_ushort(10))  # Version Major, Current and Minor
		packet.write(c_ushort(64))
		user_key = (str(uuid.uuid4()))[0:20]
		packet.write(user_key, allocated_length=33)
		packet.write(game_types.String(game.get_config("redirect_address"), allocated_length=33))  # World Instance IP
		packet.write(game_types.String(game.get_config("redirect_address"), allocated_length=33))  # Chat Instance IP
		packet.write(c_uint16(2002))  # World Port
		packet.write(c_ushort(3003))  # Chat Port
		packet.write(game_types.String('0', allocated_length=33))  # Some other IP
		packet.write(game_types.String('00000000-0000-0000-0000-000000000000', allocated_length=37))
		packet.write(c_ulong(0))
		packet.write(game_types.String('US', allocated_length=3))  # US Localization
		packet.write(c_bool(False))
		packet.write(c_bool(False))
		packet.write(c_ulonglong(0))
		packet.write("Hello there ;D", length_type=c_uint16)  # Custom error message
		packet.write(c_uint16(0))
		packet.write(c_ulong(4))

		self.send(packet, address)

		if (login):
			session_service = game.get_service("Session")
			player_service = game.get_service("Player")
			player_service.add_account(account_id=user_info[0]["account_id"])
			session_service.add_session(address=address, user_key=user_key, account_id=user_info[0]["account_id"], username=username)

	def handle_packet(self, data : bytes, address : pyraknet.messages.Address):
		game.trigger_event("OnPacket_Auth_{}".format(str(data[0:8])), args=[data[8:], address], debug=True)






################
#Created by lcdr
################
import asyncio
import socket
import time

from DBHandlers import *
from bitstream import *
from reliability import PacketReliability, ReliabilityLayer
from messages import Message
from Packet import LegoPackets

class Server:
	def __init__(self, address, DB, max_connections, incoming_password, role="SERVER"):
		host, port = address
		if host == "localhost":
			host = "127.0.0.1"
		self._address = host, port

		self.role = role
		self.consoleMessage = []
		self.DB = DB

		self.max_connections = max_connections
		self.incoming_password = incoming_password
		self._connected = {}
		self.handlers = {}
		self.not_console_logged_packets = set(("InternalPing", "ConnectedPong"))
		self.file_logged_packets = set()

		asyncio.ensure_future(self.init_network())
		asyncio.ensure_future(self._check_connections_loop())

		self.register_handler(Message.ConnectionRequest, self.on_connection_request)
		self.register_handler(Message.NewIncomingConnection, self.on_new_connection)
		self.register_handler(Message.InternalPing, self.on_internal_ping)
		self.register_handler(Message.DisconnectionNotification, self.on_disconnect_or_connection_lost)
		self.register_handler(Message.ConnectionLost, self.on_disconnect_or_connection_lost)
		self.log("Started up")

	@asyncio.coroutine
	def init_network(self):
		loop = asyncio.get_event_loop()
		self._transport, protocol = yield from (loop.create_datagram_endpoint(lambda: self, local_addr=self._address))
		self._address = self._transport.get_extra_info("sockname")

	# Protocol methods

	@staticmethod
	def connection_lost(exc):
		print(exc)

	def log(self, msg):
		#self.consoleMessage.append(msg)
		print("[" + self.role + "]" + msg)

	@staticmethod
	def error_received(exc):
		print(exc, vars(exc))

	def connection_made(self, transport):
		self._transport = transport

	@staticmethod
	def pause_writing():
		print("Sending too much, getting throttled")

	@staticmethod
	def resume_writing():
		print("Sending is within limits again")

	def datagram_received(self, data, address):
		if len(data) <= 2: # If the length is leq 2 then this is a raw datagram
			if data[0] == Message.OpenConnectionRequest:
				self.on_open_connection_request(address)
		else:
			if address in self._connected:
				for packet in self._connected[address].handle_datagram(data):
					self.on_packet(packet, address)

	@asyncio.coroutine
	def _check_connections_loop(self):
		while True:
			for address, layer in self._connected.copy().items():
				if layer._resends and layer.last_ack_time < time.time() - 10:
					self.close_connection(address)
			yield from asyncio.sleep(10)

	# Sort of API methods

	def close_connection(self, address):
		if address in self._connected:
			DisconnectionNotify = BitStream()
			# START OF HEADER
			DisconnectionNotify.write(bytes(Message.LegoPacket))  # MSG ID
			DisconnectionNotify.write(bytes(0x00))  # Connection Type
			DisconnectionNotify.write(bytes(0x00))  # Internal Packet ID
			DisconnectionNotify.write(bytes(0x00))  # Unknown
			###END OF HEADER
			DisconnectionNotify.write(c_ulong(0x00))  # Unknown Server Error
			self.send(DisconnectionNotify)
			self.on_packet(bytes((Message.DisconnectionNotification,)), address)
		else:
			self.log("Tried closing connection to someone we are not connected to! (Todo: Implement the router)")

	def send(self, data, address=None, broadcast=False, reliability=PacketReliability.ReliableOrdered, ignoreConnection=False):
		assert reliability != PacketReliability.ReliableSequenced # If you need this one, tell me
		if broadcast:
			recipients = self._connected.copy()
			if address is not None:
				del recipients[address]
			for recipient in recipients:
				self.send(data, recipient, False, reliability)
			return
		if address is None:
			print("No address was given!")
			return
		if address not in self._connected:
			self.log("Sending to someone we are not connected to!")
			return
		#if(self.packetname(data) not in self.not_console_logged_packets):
			#print("["+self.role+"]"+"Sending data: ")
			#print(data)
		self._connected[address].send(data, reliability)

	# Overridable hooks

	@staticmethod
	def packetname(data):
		"""String name of the packet for logging. If the name is not known, ValueError should be returned, in which case unknown_packetname will be called"""
		try:
			return Message(data[0]).name
		except Exception as e:
			print("Error while finding msg name : " + str(e))

	@staticmethod
	def unknown_packetname(data):
		"""Called when a packet name is unknown (see above). This should not throw an exception."""
		return "%.2x" % data[0]

	@staticmethod
	def packet_id(data):
		return data[0]

	@staticmethod
	def handler_data(data):
		"""For cutting off headers that the handler already knows and are therefore redundant."""
		return data[1:]

	# Handler stuff

	def register_handler(self, packet_id, handler, origin=None):
		handlers = self.handlers.setdefault(packet_id, [])
		handlers.append((handler, origin))


	def on_packet(self, data, address):
		handlers = self.handlers.get(self.packet_id(data), ())
		origin_handlers = [i for i in handlers if i[1] is None or i[1] == address]
		if not origin_handlers:
			self.log("No handlers for the previously received message")

		data = self.handler_data(data)
		for handler_tuple in origin_handlers:
			handler, origin_filter = handler_tuple
			stream = BitStream(data)
			if asyncio.iscoroutinefunction(handler):
				asyncio.ensure_future(handler(stream, address))
			else:
				handler(stream, address)

	# Packet callbacks

	def on_open_connection_request(self, address):
		if len(self._connected) < self.max_connections:
			if address not in self._connected:
				self._connected[address] = ReliabilityLayer(self._transport, address)
			self._transport.sendto(bytes((Message.OpenConnectionReply, 0)), address)
		else:
			raise NotImplementedError

	def on_connection_request(self, data, address):
		packet_password = data
		if self.incoming_password == packet_password:
			response = BitStream()
			response.write(c_ubyte(Message.ConnectionRequestAccepted))
			response.write(socket.inet_aton(address[0]))
			response.write(c_ushort(address[1]))
			response.write(bytes(2)) # Connection index, seems like this was right out ignored in RakNet
			response.write(socket.inet_aton(self._address[0]))
			response.write(c_ushort(self._address[1]))
			self.send(response, address, reliability=PacketReliability.Reliable)
		else:
			raise NotImplementedError

	def on_new_connection(self, data, address):
		self.log("New Connection from " + str(address))

	def on_internal_ping(self, data, address):
		ping_send_time = data[:4]

		pong = BitStream()
		pong.write(c_ubyte(Message.ConnectedPong))
		pong.write(ping_send_time)
		pong.write(c_uint(int(time.perf_counter() * 1000)))
		self.send(pong, address, PacketReliability.Unreliable)

	def on_disconnect_or_connection_lost(self, data, address):
		DisconnectionNotify = BitStream()
		# START OF HEADER
		DisconnectionNotify.write(bytes(Message.LegoPacket))  # MSG ID
		DisconnectionNotify.write(bytes(0x00))  # Connection Type
		DisconnectionNotify.write(bytes(0x00))  # Internal Packet ID
		DisconnectionNotify.write(bytes(0x00))  # Unknown
		###END OF HEADER
		DisconnectionNotify.write(c_ulong(0x00))  # Unknown Server Error
		self.send(DisconnectionNotify, address)
		self.log("Disconnect/Connection lost to %s" % str(address))
		self._connected[address].stop = True
		del self._connected[address]
		# Remove any registered handlers associated with the disconnected address
		for packet_type in self.handlers:
			handlers_to_remove = [handler for handler in self.handlers[packet_type] if handler[1] == address]
			for handler in handlers_to_remove:
				self.handlers[packet_type].remove(handler)
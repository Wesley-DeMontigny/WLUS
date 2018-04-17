################
#Created by lcdr
################
import asyncio
import math
import time
from collections import OrderedDict

import rangelist
from bitstream import BitStream, c_bit, c_uint, c_ushort

class PacketReliability:
	Unreliable = 0
	UnreliableSequenced = 1
	Reliable = 2
	ReliableOrdered = 3
	ReliableSequenced = 4

class ReliabilityLayer:
	def __init__(self, transport, address):
		self.stop = False
		self.last_ack_time = 0
		self.split_packet_id = 0
		self._remote_system_time = 0
		self._transport = transport
		self._address = address
		self._acks = rangelist.RangeList()
		self._send_message_number_index = 0
		self._sequenced_write_index = 0
		self._sequenced_read_index = 0
		self._ordered_write_index = 0
		self._ordered_read_index = 0
		self._last_received = [-1] * 50
		self._out_of_order_packets = {} # for ReliableOrdered
		self._sends = []
		self._resends = OrderedDict()

		asyncio.ensure_future(self._send_loop(is_resends=False))
		asyncio.ensure_future(self._send_loop(is_resends=True))

	def handle_datagram(self, datagram):
		stream = BitStream(datagram)
		if self.handle_datagram_header(stream):
			return # Acks only packet
 		# There can be multiple packets in one datagram
		yield from self.parse_packets(stream)

	def handle_datagram_header(self, data):
		has_acks = data.read(c_bit)
		if has_acks:
			assert data.read(c_uint) == 0 # unused
			acks = rangelist.RangeList(data)
			for message_number in acks.ranges():
				if message_number in self._resends:
					del self._resends[message_number]
			self.last_ack_time = time.time()
		if data.all_read():
			return True
		has_remote_system_time = data.read(c_bit)
		if has_remote_system_time:
			self._remote_system_time = data.read(c_uint)

	def parse_packets(self, data):
		while not data.all_read():
			message_number = data.read(c_uint)
			reliability = data.read_bits(3)[0]
			assert reliability != PacketReliability.ReliableSequenced # This is never used

			if reliability == PacketReliability.UnreliableSequenced or reliability == PacketReliability.ReliableOrdered:
				ordering_channel = data.read_bits(5)[0]
				assert ordering_channel == 0 # No one actually uses a custom ordering channel
				ordering_index = data.read(c_uint)

			is_split_packet = data.read(c_bit)
			if is_split_packet:
				raise NotImplementedError

			length = data.read(c_ushort, compressed=True)
			data.align_read()
			packet_data = data.read(bytes, length=math.ceil(length / 8))

			if reliability in (PacketReliability.Reliable, PacketReliability.ReliableOrdered):
				self._acks.append(message_number)

			if message_number not in self._last_received:
				del self._last_received[0]
				self._last_received.append(message_number)
			else:
				print("got duplicate")
				continue

			if reliability == PacketReliability.UnreliableSequenced:
				if ordering_index >= self._sequenced_read_index:
					self._sequenced_read_index = ordering_index + 1
				else:
					# Since we have already filtered duplicate packets, this should never happen
					print("Received unfiltered sequenced duplicate, increase size of _last_received!")
					continue
			elif reliability == PacketReliability.ReliableOrdered:
				if ordering_index == self._ordered_read_index:
					self._ordered_read_index += 1
					ord = ordering_index+1
					while ord in self._out_of_order_packets:
						self._ordered_read_index += 1
						yield self._out_of_order_packets.pop(ord)
						ord += 1
				elif ordering_index < self._ordered_read_index:
					# Since we have already filtered duplicate packets, this should never happen
					print("Received unfiltered ordered duplicate, increase size of _last_received!")
					continue
				else:
					# Packet arrived too early, we're still waiting for a previous packet
					# Add this one to a queue so we can process it later
					self._out_of_order_packets[ordering_index] = packet_data
			yield packet_data

	def send(self, data, reliability):
		if reliability == PacketReliability.UnreliableSequenced:
			ordering_index = self._sequenced_write_index
			self._sequenced_write_index += 1
		elif reliability == PacketReliability.ReliableOrdered:
			ordering_index = self._ordered_write_index
			self._ordered_write_index += 1
		else:
			ordering_index = None

		if ReliabilityLayer.packet_header_length(reliability, False) + len(data) >= 1492 - 28: # mtu - udp header
			data_offset = 0
			chunks = []
			while data_offset < len(data):
				data_length = 1492 - 28 - ReliabilityLayer.packet_header_length(reliability, True)
				chunks.append(data[data_offset:data_offset+data_length])
				data_offset += data_length

			split_packet_id = self.split_packet_id
			self.split_packet_id += 1
			for split_packet_index, chunk in enumerate(chunks):
				self._sends.append((chunk, reliability, ordering_index, split_packet_id, split_packet_index, len(chunks)))
		else:
			self._sends.append((data, reliability, ordering_index, None, None, None))

	@asyncio.coroutine
	def _send_loop(self, is_resends):
		if is_resends:
			queue = self._resends
			interval = 1
		else:
			queue = self._sends
			interval = 0.03

		while True:
			if self.stop:
				break
			queue_copy = queue.copy()
			for i in queue_copy:
				if is_resends:
					message_number = i
					data, reliability, ordering_index, split_packet_id, split_packet_index, split_packet_count = queue_copy[i]
				else:
					data, reliability, ordering_index, split_packet_id, split_packet_index, split_packet_count = i
					message_number = self._send_message_number_index
					self._send_message_number_index += 1

				out = BitStream()
				out.write(c_bit(len(self._acks) != 0))
				if self._acks:
					out.write(c_uint(self._remote_system_time))
					out.write(self._acks.serialize())
					self._acks.clear()

				if len(out) + ReliabilityLayer.packet_header_length(reliability, split_packet_id != None) + len(data) > 1492:
					continue

				has_remote_system_time = False # time is only used for us to get back to calculate ping, and we don't do that
				out.write(c_bit(has_remote_system_time))
				#out.write(c_uint(remote_system_time))

				out.write(c_uint(message_number))

				out.write_bits(reliability.to_bytes(length=1, byteorder="little"), 3)

				if reliability in (PacketReliability.UnreliableSequenced, PacketReliability.ReliableOrdered):
					out.write_bits(b"\0", 5) # ordering_channel, no one ever uses anything else than 0
					out.write(c_uint(ordering_index))

				is_split_packet = split_packet_id != None
				out.write(c_bit(is_split_packet))
				if is_split_packet:
					out.write(c_ushort(split_packet_id))
					out.write(c_uint(split_packet_index), compressed=True)
					out.write(c_uint(split_packet_count), compressed=True)
				out.write(c_ushort(len(data) * 8), compressed=True)
				out.align_write()
				out.write(data)

				assert len(out) < 1492 # maximum packet size handled by raknet
				self._transport.sendto(out, self._address)

				if not is_resends:
					if reliability == PacketReliability.Reliable or reliability == PacketReliability.ReliableOrdered:
						self._resends[message_number] = i
					self._sends.remove(i)
			if self._acks:
				out = BitStream()
				out.write(c_bit(True))
				out.write(c_uint(self._remote_system_time))
				out.write(self._acks.serialize())
				self._acks.clear()
				self._transport.sendto(out, self._address)
			yield from asyncio.sleep(interval)

	@staticmethod
	def packet_header_length(reliability, is_split_packet):
		length = 32 # message number
		length += 3 # reliability
		if reliability in (PacketReliability.UnreliableSequenced, PacketReliability.ReliableOrdered):
			length += 5 # ordering channel
			length += 32
		length += 1 # is split packet
		if is_split_packet:
			length += 16 # split packet id
			length += 32 # split packet index (actually a compressed write so assume the maximum)
			length += 32 # split packet count (actually a compressed write so assume the maximum)
		length += 16 # data length (actually a compressed write so assume the maximum)
		return math.ceil(length / 8)
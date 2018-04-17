################
#Created by lcdr
################
import math
import struct
from ctypes import *

class Struct(struct.Struct):
	# cast-like syntax for packing
	def __call__(self, value):
		return self.pack(value)

c_bool = Struct("?")
c_float = Struct("f")
c_double = Struct("d")
c_int = Struct("i")
c_uint = Struct("I")

c_char = Struct("c")
c_charArr = Struct("s")

c_byte = Struct("b")#Signed char
c_ubyte = Struct("B")#Unsigned char
c_short = Struct("h")
c_ushort = Struct("H")
c_long = Struct("l")
c_ulong = Struct("L")
c_longlong = Struct("q")
c_ulonglong = Struct("Q")

c_int8 = c_byte
c_uint8 = c_ubyte
c_int16 = c_short
c_uint16 = c_ushort
c_int32 = c_long
c_uint32 = c_ulong
c_int64 = c_longlong
c_uint64 = c_ulonglong

class c_bit:
	def __init__(self, boolean):
		self.value = boolean


def variableLength(len):
	return c_ubyte(len)

class BitStream(bytearray):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._write_offset = 0
		self._read_offset = 0

	#This was not in the initial file. It used to cause an error but now it isn't. If it starts up again just remove it and write to the packet directly
	def writeTemplate(self, arg):
		templateKeys = dir(arg)
		data = BitStream()
		for key in templateKeys:
			if(key[0:2] != "__" and callable(getattr(arg, key)) != True):
				value = getattr(arg, key)
				data.write(value)
		self.write(data)

	def write(self, arg, compressed=False, char_size:"for strings"=2, allocated_length:"for fixed-length strings"=33, length_type:"for variable-length strings"=None):
		if isinstance(arg, BitStream):
			self.write_bits(bytes(arg), arg._write_offset, align_right=False)
			return
		if isinstance(arg, c_bit):
			self._write_bit(arg.value)
			return
		if isinstance(arg, str):
			self._write_str(arg, char_size, allocated_length, length_type)
			return
		if not isinstance(arg, (bytes, bytearray)):
			raise TypeError(arg)

		if compressed:
			self._write_compressed(arg)
		else:
			self.write_bits(arg)

	def _write_str(self, str_, char_size, allocated_length, length_type):
		# possibly include default encoded lengths for non-variable-length strings (seem to be 33 for string and 66 for wstring)
		if char_size == 2:
			encoding = "utf-16-le"
		elif char_size == 1:
			encoding = "latin1"
		else:
			raise ValueError(char_size)

		encoded_string = str_.encode(encoding)

		if length_type is not None:
			# Variable-length string
			self.write(length_type(len(encoded_string))) # note: there's also a version that uses the length of the encoded string, should that be used?
		else:
			# Fixed-length string
			encoded_string += bytes(char_size) # null terminator
			if len(encoded_string) > allocated_length:
				raise ValueError("String too long! Allocated Length was " + str(allocated_length) + " but the needed length was " + str(len(encoded_string)))
			encoded_string += bytes(allocated_length-len(encoded_string))
		self.write_bits(encoded_string)

	def _write_bit(self, bit):
		self._alloc_bits(1)
		if bit: # we don't actually have to do anything if the bit is 0
			self[self._write_offset//8] |= 0x80 >> self._write_offset % 8

		self._write_offset += 1

	def write_bits(self, byte_arg, number_of_bits=None, align_right=True):
		if number_of_bits is None:
			number_of_bits = len(byte_arg) * 8
		self._alloc_bits(number_of_bits)
		offset = 0
		while number_of_bits > 0:
			data_byte = byte_arg[offset]
			if number_of_bits < 8 and align_right: # In the case of a partial byte, the bits are aligned from the right (bit 0) rather than the left (as in the normal internal representation)
				data_byte = data_byte << (8 - number_of_bits) & 0xff # Shift left to get the bits on the left, as in our internal representation
			if self._write_offset % 8 == 0:
				self[self._write_offset//8] = data_byte
			else:
				self[self._write_offset//8] |= data_byte >> self._write_offset % 8 # First half
				if 8 - self._write_offset % 8 < number_of_bits: # If we didn't write it all out in the first half (8 - self._write_offset % 8 is the number we wrote in the first half)
					self[self._write_offset//8 + 1] = (data_byte << 8 - self._write_offset % 8) & 0xff # Second half (overlaps byte boundary)
			if number_of_bits >= 8:
				self._write_offset += 8
				number_of_bits -= 8
				offset += 1
			else:
				self._write_offset += number_of_bits
				return

	def _write_compressed(self, byte_arg):
		current_byte = len(byte_arg) - 1

		# Write upper bytes with a single 1
		# From high byte to low byte, if high byte is 0 then write 1. Otherwise write 0 and the remaining bytes
		while current_byte > 0:
			is_zero = byte_arg[current_byte] == 0
			self._write_bit(is_zero)
			if not is_zero:
				# Write the remainder of the data
				self.write_bits(byte_arg, (current_byte + 1) * 8)
				return
			current_byte -= 1

		# If the upper half of the last byte is 0 then write 1 and the remaining 4 bits. Otherwise write 0 and the 8 bits.

		is_zero = byte_arg[current_byte] & 0xF0 == 0x00
		self._write_bit(is_zero)
		if is_zero:
			bits = 4
		else:
			bits = 8

		self.write_bits(byte_arg[current_byte:], bits)

	def align_write(self):
		if self._write_offset % 8 != 0:
			self._alloc_bits(8 - self._write_offset % 8)
			self._write_offset += 8 - self._write_offset % 8

	def _alloc_bits(self, number_of_bits):
		bytes_to_allocate = math.ceil((self._write_offset + number_of_bits) / 8) - len(self)
		if bytes_to_allocate > 0:
			self += bytes(bytes_to_allocate)


	def skip_read(self, byte_length):
		self._read_offset += byte_length * 8

	def read(self, arg_type, compressed=False, length:"for BitStream (in bits) and for bytes (in bytes)"=None, char_size:"for strings"=2, allocated_length:"for fixed-length strings"=33, length_type:"for variable-length strings"=None):
		if isinstance(arg_type, struct.Struct):
			if compressed:
				if arg_type in (c_float, c_double):
					raise NotImplementedError
				read = self._read_compressed(arg_type.size)
			else:
				read = self.read_bits(arg_type.size * 8)
			return arg_type.unpack(read)[0]
		if issubclass(arg_type, c_bit):
			return self._read_bit()
		if issubclass(arg_type, str):
			return self._read_str(char_size, allocated_length, length_type)
		if issubclass(arg_type, bytes):
			return self.read_bits(length * 8)
		if issubclass(arg_type, BitStream):
			return BitStream(self.read_bits(length, align_right=False))
		raise TypeError(arg_type)

	def _read_str(self, char_size, allocated_length, length_type):
		if char_size == 2:
			encoding = "utf-16-le"
		elif char_size == 1:
			encoding = "latin1"
		else:
			raise ValueError(char_size)

		if length_type is not None:
			# Variable-length string
			length = self.read(length_type)
			byte_str = self.read(bytes, length=length*char_size)
		else:
			# Fixed-length string
			byte_str = bytearray()
			while len(byte_str) < allocated_length:
				char = self.read_bits(char_size * 8)
				if sum(char) == 0:
					self.skip_read(allocated_length - len(byte_str) - char_size)
					break
				byte_str += char

		return byte_str.decode(encoding)

	def _read_bit(self):
		bit = self[self._read_offset//8] & 0x80 >> self._read_offset % 8 != 0
		self._read_offset += 1
		return bit

	def read_bits(self, number_of_bits, align_right=True):
		if self._read_offset % 8 == 0 and number_of_bits % 8 == 0: # optimization for no bitshifts
			output = self[self._read_offset//8:self._read_offset//8+number_of_bits//8]
			self._read_offset += number_of_bits
			return output

		output = bytearray(math.ceil(number_of_bits / 8))
		offset = 0
		while number_of_bits > 0:
			output[offset] |= (self[self._read_offset//8] << self._read_offset % 8) & 0xff # First half
			if self._read_offset % 8 != 0 and number_of_bits > 8 - self._read_offset % 8: # If we have a second half, we didn't read enough bytes in the first half
				output[offset] |= self[self._read_offset//8 + 1] >> 8 - self._read_offset % 8 # Second half (overlaps byte boundary)
			self._read_offset += 8
			if number_of_bits >= 8:
				number_of_bits -= 8
			else:
				number_of_unread_bits = 8 - number_of_bits
				if align_right:
					output[offset] >>= number_of_unread_bits
				self._read_offset -= number_of_unread_bits
				break
			offset += 1
		return output

	def _read_compressed(self, number_of_bytes):
		current_byte = number_of_bytes - 1

		while current_byte > 0:
			if self._read_bit():
				current_byte -= 1
			else:
				# Read the rest of the bytes
				return bytearray(number_of_bytes - current_byte - 1) + self.read_bits((current_byte + 1) * 8)

		# All but the first bytes are 0. If the upper half of the last byte is a 0 (positive) or 16 (negative) then what we read will be a 1 and the remaining 4 bits.
		# Otherwise we read a 0 and the 8 bits
		if self._read_bit():
			bits = 4
		else:
			bits = 8
		return self.read_bits(bits) + bytearray(number_of_bytes - current_byte - 1)

	def align_read(self):
		if self._read_offset % 8 != 0:
			self._read_offset += 8 - self._read_offset % 8

	def all_read(self):
		# This is not accurate to the bit, just to the byte
		return math.ceil(self._read_offset / 8) == len(self)

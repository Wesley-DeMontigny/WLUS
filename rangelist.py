################
#Created by lcdr
################
from bitstream import BitStream, c_bit, c_uint, c_ushort

class RangeList(list):
	"""
	List that stores things and compresses them to ranges if possible.
	To add an item, use append (does not necessarily add to the end).
	To get the uncompressed ranges, use ranges.
	Any other methods operate on the internal representation and not items, avoid using them if you don't need them.

	Internal:
		The internal list of ranges is auto-sorted.
		Ranges in the internal representation are inclusive from both ends (that is, (20, 25) contains both 20 and 25 and everything in between)
	"""

	def __init__(self, input_stream=None):
		"""Init the rangelist, optionally by deserializing from a bitstream."""
		super().__init__()
		if input_stream is not None:
			count = input_stream.read(c_ushort, compressed=True)
			for _ in range(count):
				max_equal_to_min = input_stream.read(c_bit)
				min = input_stream.read(c_uint)
				if max_equal_to_min:
					max = min
				else:
					max = input_stream.read(c_uint)
				super().append((min, max))

	def ranges(self):
		"""Yield the numbers in the ranges, basically uncompressing the ranges."""
		for min, max in self:
			yield from range(min, max + 1)

	def append(self, item):
		iter_ = iter(self)
		for range in iter_:
			if range[0] == item + 1: # The item can extend the range
				range[0] -= 1
				break
			if range[0] <= item:
				if range[1] == item - 1: # The item can extend the range
					range[1] += 1
					try:
						nextrange = next(iter_)
						if nextrange[0] == item + 1: # The newly updated list has a max of one less than the next list, in which case we can merge these
							# Merge the ranges
							range[1] = nextrange[1]
							self.remove(nextrange)
					except StopIteration:
						pass
					break
				if range[1] >= item: # The item is within the range, we don't even need to update it
					break
				continue # The item is higher than the current range, check next range
			# If we got here, the range starts at a higher position than the item, so we should insert it now (the list is auto-sorted so there can't be any other position)
			super().insert(self.index(range), [item, item])
			break
		else:
			# We ran through the whole list and couldn't find a good existing range
			super().append([item, item])

	def serialize(self):
		"""
		Serialize the RangeList. This is meant to be compatible with RakNet's serialization.
		(This currently serializes items as uints, since currently the only occurence where I need to serialize a rangelist is with an uint)
		"""
		out = BitStream()
		out.write(c_ushort(len(self)), compressed=True)
		for range in self:
			out.write(c_bit(range[0] == range[1]))
			out.write(c_uint(range[0]))
			if range[0] != range[1]:
				out.write(c_uint(range[1]))
		return out

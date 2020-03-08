"""
Contains all the packets that the world/char server would send to the client
"""
from pyraknet import bitstream


class MinfigureListPacket(bitstream.Serializable):
    """
    [53-05-00-06]
    This sends all of the characters to the client.
    """
    def __init__(self):
        self.current_index = 0
        self.minifigs = []

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This packet cannot be deserialized")

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(bitstream.c_uint8(len(self.minifigs)))
        stream.write(bitstream.c_uint8(self.current_index))
        for m in self.minifigs:
            stream.write(m)


class MinifigureCreationResponsePacket(bitstream.Serializable):
    """
    [53-05-00-07]
    Lets the client know how the creation process was handled.
    """
    def __init__(self):
        self.response = 0x00

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This packet cannot be deserialized")

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(bitstream.c_uint8(self.response))


class RedirectiontoNewServerPacket(bitstream.Serializable):
    """
    [53-05-00-0e]
    This packet redirects the client to connect to a new server.
    If worlds are hosted on separate servers, send this packet and
    let the other server handle the load world packet. It would
    probably be best if the other server sent the load world on
    handshake - because when would there be a connection which wasn't
    trying to load in the world.
    """

    def __init__(self):
        self.redirect_ip = "127.0.0.1"
        self.redirect_port = 1124
        self.is_mythran_dimension_shift = False

    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This packet cannot be deserialized")

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(self.redirect_ip, allocated_length=33)
        stream.write(bitstream.c_uint16(self.redirect_port))
        stream.write(bitstream.c_bool(self.is_mythran_dimension_shift))

"""
Contains all the packets that the world/char server would send to the client
"""
from pyraknet import bitstream
from plugins.serializables.misc_serializables import CString, Vector3, LUZ, LDF
from plugins.easy_cdclient.cdclient_objects import Zone
import zlib


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

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This packet cannot be deserialized")

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(CString(self.redirect_ip, allocated_length=33))
        stream.write(bitstream.c_uint16(self.redirect_port))
        stream.write(bitstream.c_bool(self.is_mythran_dimension_shift))


class WorldInfoPacket(bitstream.Serializable):
    """
    [53-05-00-02]
    This packet tells the client what zone to load.
    """

    def __init__(self):
        self.zone_id = 0
        self.map_instance = 0
        self.map_clone = 0
        self.map_checksum = 0
        self.editor_enabled = False
        self.editor_level = 0
        self.player_position = Vector3()
        self.activity = 0  # If in battle put 4??

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This packet cannot be deserialized")

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(bitstream.c_uint16(self.zone_id))
        stream.write(bitstream.c_uint16(self.map_instance))
        stream.write(bitstream.c_uint32(self.map_clone))
        stream.write(bitstream.c_uint32(self.map_checksum))
        stream.write(bitstream.c_bool(self.editor_enabled))
        stream.write(bitstream.c_uint8(self.editor_level))
        stream.write(self.player_position)
        stream.write(bitstream.c_uint32(self.activity))

    @classmethod
    def from_cdclient(cls, zone_id, default_spawn=False) -> "WorldInfoPacket":
        generated_zone = Zone(zone_id)
        world_info = WorldInfoPacket()
        world_info.zone_id = zone_id
        world_info.map_checksum = generated_zone.checksum
        if default_spawn:
            file = "./res/maps/" + str(generated_zone.zone_data.zoneName)
            luz_file = open(file, "rb")
            stream = bitstream.ReadStream(luz_file.read())
            luz = stream.read(LUZ)
            world_info.player_position = luz.spawnpoint_position
        return world_info


class DetailedUserInfoPacket(bitstream.Serializable):
    """
    [53-05-00-04]
    Send after client load complete packet
    """

    def __init__(self):
        self.ldf = LDF()

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This packet cannot be deserialized")

    def serialize(self, stream: bitstream.WriteStream) -> None:
        temp_stream = bitstream.WriteStream()
        temp_stream.write(self.ldf)
        temp_bytes = temp_stream.__bytes__()
        compressed_bytes = zlib.compress(temp_bytes)
        stream.write(bitstream.c_ulong(len(compressed_bytes) + 9))
        stream.write(bitstream.c_bool(True))
        stream.write(bitstream.c_ulong(len(temp_bytes)))
        stream.write(bitstream.c_ulong(len(compressed_bytes)))
        stream.write(compressed_bytes)

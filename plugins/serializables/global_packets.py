"""
Contains all the packets which are sent by either the client or server
"""
from pyraknet import bitstream


class HandshakePacket(bitstream.Serializable):
    """
    [53-00-00-00]
    Global handshake packet serializable.
    This packet is sent to establish a connection.
    """
    def __init__(self):
        self.game_version = 171022
        self.unknown_0 = 0
        self.remote_connection_type = 0  # For auth this is 1, otherwise it is 4
        self.process_id = 1124
        self.local_port = 0xff

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(bitstream.c_uint32(self.game_version))
        stream.write(bitstream.c_uint32(self.unknown_0))
        stream.write(bitstream.c_uint32(self.remote_connection_type))
        stream.write(bitstream.c_uint32(self.process_id))
        stream.write(bitstream.c_uint16(self.local_port))
        stream.write("127.0.0.1", allocated_length=33)

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = HandshakePacket()
        packet.game_version = stream.read(bitstream.c_uint32)
        packet.unknown_0 = stream.read(bitstream.c_uint32)
        packet.remote_connection_type = stream.read(bitstream.c_uint32)
        packet.process_id = stream.read(bitstream.c_uint32)
        packet.local_port = stream.read(bitstream.c_uint16)
        return packet


class DisconnectNotifyPacket(bitstream.Serializable):
    """
    [53-00-00-01]
    This packet is sent when the server and client disconnect from each other
    """
    def __init__(self):
        self.disconnect_id = 0

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(bitstream.c_uint32(self.disconnect_id))

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = DisconnectNotifyPacket()
        packet.disconnect_id = stream.read(bitstream.c_uint32)
        return packet

    def send(self, generic_game_server, address):
        disconnect_packet = bitstream.WriteStream()
        disconnect_packet.write(b"S\x00\x00\x01\x00\x00\x00\x00")
        disconnect_packet.write(self)
        generic_game_server.send(disconnect_packet, address)
        generic_game_server.delete_session(ip_address=address[0])


class GeneralNotifyPacket(bitstream.Serializable):
    """
    [53-00-00-02]
    This packet is sent to notify the player?
    """
    def __init__(self):
        self.notify_id = 0

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(bitstream.c_uint32(self.notify_id))

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = GeneralNotifyPacket()
        packet.notify_id = stream.read(bitstream.c_uint32)
        return packet

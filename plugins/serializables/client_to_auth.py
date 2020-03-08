"""
Contains all the packets that are sent from the client to the auth server.
"""
from pyraknet import bitstream


class LoginInfoPacket(bitstream.Serializable):
    """
    [53-01-00-00]
    This packet contains the username and password of a player logging in.
    Even though there is more information in the Login Info Packet,
    the only ones that this Serializable will read is the Username and Password
    """
    def __init__(self):
        self.username = ""
        self.password = ""

    def serialize(self, stream: bitstream.WriteStream) -> None:
        raise Exception("This Serializable can only deserialize")

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = LoginInfoPacket()
        packet.username = stream.read(str, allocated_length=33)
        packet.password = stream.read(str, allocated_length=41)
        return packet





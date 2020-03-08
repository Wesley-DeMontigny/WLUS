"""
Contains all the packets that auth would send to the client
"""
from pyraknet import bitstream
from .misc_serializables import CString


class LoginInfoPacket(bitstream.Serializable):
    """
    [53-05-00-00]
    This packet is sent in response to the character logging in.
    """
    def __init__(self):
        self.login_return_code = 0x06
        self.client_version_major = 1
        self.client_version_current = 10
        self.client_version_minor = 64
        self.user_key = ""
        self.char_ip = "127.0.0.1"
        self.chat_ip = "127.0.0.1"
        self.char_port = 2002
        self.chat_port = 3003
        self.localization = "US"
        self.custom_error = ""
        self.display_first_time = False
        self.is_ftp = False

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(bitstream.c_uint8(self.login_return_code))
        stream.write(CString("Talk_Like_A_Pirate", allocated_length=33))
        stream.write(CString("", allocated_length=33 * 7))
        stream.write(bitstream.c_uint16(self.client_version_major))
        stream.write(bitstream.c_uint16(self.client_version_current))
        stream.write(bitstream.c_uint16(self.client_version_minor))
        stream.write(self.user_key, allocated_length=33)
        stream.write(CString(self.char_ip, allocated_length=33))
        stream.write(CString(self.chat_ip, allocated_length=33))
        stream.write(bitstream.c_uint16(self.char_port))
        stream.write(bitstream.c_uint16(self.chat_port))
        stream.write(CString('0', allocated_length=33))
        stream.write(CString('00000000-0000-0000-0000-000000000000', allocated_length=37))
        stream.write(bitstream.c_uint32(0))
        stream.write(CString(self.localization, allocated_length=3))  # US Localization
        stream.write(bitstream.c_bool(self.display_first_time))
        stream.write(bitstream.c_bool(self.is_ftp))
        stream.write(bitstream.c_uint64(0))
        stream.write(self.custom_error, length_type=bitstream.c_uint16)  # Custom error message
        stream.write(bitstream.c_uint16(0))
        stream.write(bitstream.c_uint32(4))

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This packet cannot be deserialized.")

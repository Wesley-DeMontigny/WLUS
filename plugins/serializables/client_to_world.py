"""
Contains all the packets sent from the client to the world/char server
"""
from pyraknet import bitstream
from ..serializables import misc_serializables, packet_enum


class UserSessionInfoPacket(bitstream.Serializable):
    """
    [53-04-00-01]
    This packet contains the username and session key of a user who went through
    the auth server.
    """
    def __init__(self):
        self.username = ""
        self.user_key = ""

    def serialize(self, stream: bitstream.WriteStream) -> None:
        raise Exception("This Serializable can only deserialize")

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = UserSessionInfoPacket()
        packet.username = stream.read(str, allocated_length=33)
        packet.user_key = stream.read(str, allocated_length=33)
        return packet


class MinifigureListRequestPacket(bitstream.Serializable):
    """
    [53-04-00-02]
    This packet actually doesn't have any info. It's just here because it exists.
    This is sent to let the server know that it's ready for the minifgure list
    """
    def serialize(self, stream: bitstream.WriteStream) -> None:
        raise Exception("This Serializable can only deserialize")

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = UserSessionInfoPacket()
        return packet


class MinifigureCreateRequestPacket(bitstream.Serializable):
    """
    [53-04-00-03]
    This packet is sent when a character clicks the create minfigure button.
    It contains all of the selection choices he/she made.
    """
    def __init__(self):
        self.name = ""
        self.predef_name_1 = 0
        self.predef_name_2 = 0
        self.predef_name_3 = 0
        self.unknown_0 = 0
        self.head_color = 0
        self.head = 0
        self.chest_color = 0
        self.chest = 0
        self.legs = 0
        self.hair_style = 0
        self.hair_color = 0
        self.left_hand = 0
        self.right_hand = 0
        self.eyebrow_style = 0
        self.eyes_style = 0
        self.mouth_style = 0

    def serialize(self, stream: bitstream.WriteStream) -> None:
        raise Exception("This Serializable can only deserialize")

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = MinifigureCreateRequestPacket()
        packet.name = stream.read(str, allocated_length=33)
        packet.predef_name_1 = stream.read(bitstream.c_uint32)
        packet.predef_name_2 = stream.read(bitstream.c_uint32)
        packet.predef_name_3 = stream.read(bitstream.c_uint32)
        packet.unknown_0 = stream.read(bitstream.c_uint8)
        packet.head_color = stream.read(bitstream.c_uint32)
        packet.head = stream.read(bitstream.c_uint32)
        packet.chest_color = stream.read(bitstream.c_uint32)
        packet.chest = stream.read(bitstream.c_uint32)
        packet.legs = stream.read(bitstream.c_uint32)
        packet.hair_style = stream.read(bitstream.c_uint32)
        packet.hair_color = stream.read(bitstream.c_uint32)
        packet.left_hand = stream.read(bitstream.c_uint32)
        packet.right_hand = stream.read(bitstream.c_uint32)
        packet.eyebrow_style = stream.read(bitstream.c_uint32)
        packet.eyes_style = stream.read(bitstream.c_uint32)
        packet.mouth_style = stream.read(bitstream.c_uint32)
        return packet

    def to_login_character(self):
        char = misc_serializables.LoginCharacter()
        first = open('./res/minifigname_first.txt', 'r')
        safe_name = first.readlines()[self.predef_name_1].rstrip()
        first.close()
        middle = open('./res/minifigname_middle.txt', 'r')
        safe_name += middle.readlines()[self.predef_name_2].rstrip()
        middle.close()
        last = open('./res/minifigname_last.txt', 'r')
        safe_name += last.readlines()[self.predef_name_3].rstrip()
        last.close()
        char.object_id = misc_serializables.LwoObjID.gen_lwoobjid(persistent=True, character=True)
        char.current_name = safe_name
        char.unapproved_name = self.name
        char.head_color = self.head_color
        char.head = self.head
        char.chest_color = self.chest_color
        char.chest = self.chest
        char.legs = self.legs
        char.hair_style = self.hair_style
        char.hair_color = self.hair_color
        char.left_hand = self.left_hand
        char.right_hand = self.right_hand
        char.eyebrows_style = self.eyebrow_style
        char.eyes_style = self.eyes_style
        char.mouth_style = self.mouth_style

        shirt_id = 0
        if self.chest_color == 0:
            if self.chest >= 35:
                shirt_id = 5730
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_BRIGHT_RED.value
        elif self.chest_color == 1:
            if self.chest >= 35:
                shirt_id = 5736
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_BRIGHT_BLUE.value
        elif self.chest_color == 3:
            if self.chest >= 35:
                shirt_id = 5808
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_DARK_GREEN.value
        elif self.chest_color == 5:
            if self.chest >= 35:
                shirt_id = 5754
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_BRIGHT_ORANGE.value
        elif self.chest_color == 6:
            if self.chest >= 35:
                shirt_id = 5760
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_BLACK.value
        elif self.chest_color == 7:
            if self.chest >= 35:
                shirt_id = 5766
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_DARK_STONE_GRAY.value
        elif self.chest_color == 8:
            if self.chest >= 35:
                shirt_id = 5772
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_MEDIUM_STONE_GRAY.value
        elif self.chest_color == 9:
            if self.chest >= 35:
                shirt_id = 5778
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_REDDISH_BROWN.value
        elif self.chest_color == 10:
            if self.chest >= 35:
                shirt_id = 5784
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_WHITE.value
        elif self.chest_color == 11:
            if self.chest >= 35:
                shirt_id = 5802
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_MEDIUM_BLUE.value
        elif self.chest_color == 13:
            if self.chest >= 35:
                shirt_id = 5796
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_DARK_RED.value
        elif self.chest_color == 14:
            if self.chest >= 35:
                shirt_id = 5802
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_EARTH_BLUE.value
        elif self.chest_color == 15:
            if self.chest >= 35:
                shirt_id = 5808
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_EARTH_GREEN.value
        elif self.chest_color == 16:
            if self.chest >= 35:
                shirt_id = 5814
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_BRICK_YELLOW.value
        elif self.chest_color == 84:
            if self.chest >= 35:
                shirt_id = 5820
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_SAND_BLUE.value
        elif self.chest_color == 96:
            if self.chest >= 35:
                shirt_id = 5826
            else:
                shirt_id = packet_enum.CreationLOT.SHIRT_SAND_GREEN.value

        if self.chest >= 35:
            final_shirt_id = shirt_id + (self.chest - 35)
        else:
            final_shirt_id = shirt_id + (self.chest - 1)

        if self.legs == 0:
            pants_id = packet_enum.CreationLOT.PANTS_BRIGHT_RED.value
        elif self.legs == 1:
            pants_id = packet_enum.CreationLOT.PANTS_BRIGHT_BLUE.value
        elif self.legs == 3:
            pants_id = packet_enum.CreationLOT.PANTS_DARK_GREEN.value
        elif self.legs == 5:
            pants_id = packet_enum.CreationLOT.PANTS_BRIGHT_ORANGE.value
        elif self.legs == 6:
            pants_id = packet_enum.CreationLOT.PANTS_BLACK.value
        elif self.legs == 7:
            pants_id = packet_enum.CreationLOT.PANTS_DARK_STONE_GRAY.value
        elif self.legs == 8:
            pants_id = packet_enum.CreationLOT.PANTS_MEDIUM_STONE_GRAY.value
        elif self.legs == 9:
            pants_id = packet_enum.CreationLOT.PANTS_REDDISH_BROWN.value
        elif self.legs == 10:
            pants_id = packet_enum.CreationLOT.PANTS_WHITE.value
        elif self.legs == 11:
            pants_id = packet_enum.CreationLOT.PANTS_MEDIUM_BLUE.value
        elif self.legs == 13:
            pants_id = packet_enum.CreationLOT.PANTS_DARK_RED.value
        elif self.legs == 14:
            pants_id = packet_enum.CreationLOT.PANTS_EARTH_BLUE.value
        elif self.legs == 15:
            pants_id = packet_enum.CreationLOT.PANTS_EARTH_GREEN.value
        elif self.legs == 16:
            pants_id = packet_enum.CreationLOT.PANTS_BRICK_YELLOW.value
        elif self.legs == 84:
            pants_id = packet_enum.CreationLOT.PANTS_SAND_BLUE.value
        elif self.legs == 96:
            pants_id = packet_enum.CreationLOT.PANTS_SAND_GREEN.value
        else:
            pants_id = 2508

        char.equipped_items.append(pants_id)
        char.equipped_items.append(final_shirt_id)

        return char


class JoinWorldPacket(bitstream.Serializable):
    """
    [53-04-00-04]
    This packet is sent when a user clicks play.
    """
    def __init__(self):
        self.object_id = 0

    def serialize(self, stream: bitstream.WriteStream) -> None:
        raise Exception("This Serializable can only deserialize")

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = JoinWorldPacket()
        packet.object_id = stream.read(bitstream.c_int64)
        return packet


class CharacterDeleteRequestPacket(bitstream.Serializable):
    """
    [53-04-00-06]
    This packet is sent when a user deletes a character.
    """
    def __init__(self):
        self.object_id = 0

    def serialize(self, stream: bitstream.WriteStream) -> None:
        raise Exception("This Serializable can only deserialize")

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = CharacterDeleteRequestPacket()
        packet.object_id = stream.read(bitstream.c_int64)
        return packet


class CharacterRenameRequestPacket(bitstream.Serializable):
    """
    [53-04-00-07]
    This packet is sent when a user attempts to rename their character.
    """
    def __init__(self):
        self.object_id = 0
        self.new_name = ""

    def serialize(self, stream: bitstream.WriteStream) -> None:
        raise Exception("This Serializable can only deserialize")

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = CharacterRenameRequestPacket()
        packet.object_id = stream.read(bitstream.c_int64)
        packet.new_name = stream.read(str, allocated_length=33)
        return packet


class ClientLoadCompletePacket(bitstream.Serializable):
    """
    [53-04-00-13]
    This packet is sent when the client is finished loading.
    """
    def __init__(self):
        self.zone_id = 0
        self.map_instance = 0
        self.map_clone = 0

    def serialize(self, stream: bitstream.WriteStream) -> None:
        raise Exception("This Serializable can only deserialize")

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        packet = ClientLoadCompletePacket()
        packet.zone_id = stream.read(bitstream.c_uint16)
        packet.map_instance = stream.read(bitstream.c_uint16)
        packet.map_clone = stream.read(bitstream.c_uint32)
        return packet



from pyraknet import bitstream
import random
import sqlite3
from xml.etree import ElementTree


class CString(bitstream.Serializable):
    def __init__(self, data='', allocated_length=None, length_type=None):
        self.data = data
        self.allocated_length = allocated_length
        self.length_type = length_type

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(self.data if isinstance(self.data, bytes) else bytes(self.data, 'latin1'),
                     allocated_length=self.allocated_length, length_type=self.length_type)

    def deserialize(self, stream: bitstream.ReadStream):
        return stream.read(bytes, allocated_length=self.allocated_length, length_type=self.length_type).decode('latin1')


class LwoObjID:
    """
    This is the data type that object ids are made out of.
    They are different from normal 64 bit ints because they have flags that must be set.
    """
    @classmethod
    def gen_lwoobjid(cls, persistent: bool = False, client: bool = False, spawned: bool = False,
                     character: bool = False):
        number = random.randrange(0, (2**32) - 1)
        number = number | (int(persistent) << 32)
        number = number | (int(client) << 46)
        number = number | (int(spawned) << 58)
        number = number | (int(character) << 60)
        return number


class LDF(bitstream.Serializable):
    """
    Lego Data Format
    """
    def __init__(self):
        self._keys: list = []

    def register_key(self, key_name: str, value: any, value_type: int):
        self._keys.append([key_name, value, value_type])

    def serialize(self, stream: bitstream.WriteStream) -> None:
        key_num = len(self._keys)
        stream.write(bitstream.c_uint(key_num))
        for key in self._keys:
            name = key[0]
            value = key[1]
            value_type = key[2]
            stream.write(bitstream.c_uint8(len(name) * 2))
            for char in name:
                stream.write(char.encode('latin1'))
                stream.write(b'\0')
            stream.write(bitstream.c_ubyte(value_type))
            if value_type == 0:
                stream.write(value, length_type=bitstream.c_uint)
            elif value_type == 1:
                stream.write(bitstream.c_int(value))
            elif value_type == 3:
                stream.write(bitstream.c_float(value))
            elif value_type == 5:
                stream.write(bitstream.c_uint(value))
            elif value_type == 7:
                stream.write(bitstream.c_bool(value))
            elif value_type == 8 or value_type == 9:
                stream.write(bitstream.c_int64(value))
            elif value_type == 13:
                xml_str = bytes(ElementTree.tostring(value))
                xml_str = b'<?xml version="1.0">' + xml_str
                stream.write(bitstream.c_ulong(xml_str.__len__()))
                stream.write(xml_str)

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This struct cannot be deserialized")


class LoginCharacter(bitstream.Serializable):
    """
    This is a serializable that creates the struct which is repeated in the minfigure list packet
    """
    def __init__(self):
        self.object_id = 1124
        self.current_name = ""
        self.unapproved_name = ""
        self.name_rejected = False
        self.is_ftp = False
        self.head_color = 0
        self.head = 0
        self.chest_color = 0
        self.chest = 0
        self.legs = 0
        self.hair_style = 0
        self.hair_color = 0
        self.left_hand = 0
        self.right_hand = 0
        self.eyebrows_style = 0
        self.eyes_style = 0
        self.mouth_style = 0
        self.last_zone = 0
        self.last_map_instance = 0
        self.last_map_clone = 0
        self.equipped_items = []

    @classmethod
    def deserialize(cls, stream: bitstream.ReadStream) -> bitstream.Serializable:
        raise Exception("This struct cannot be deserialized")

    def serialize(self, stream: bitstream.WriteStream) -> None:
        stream.write(bitstream.c_uint64(self.object_id))
        stream.write(bitstream.c_uint32(0))
        stream.write(self.current_name, allocated_length=33)
        stream.write(self.unapproved_name, allocated_length=33)
        stream.write(bitstream.c_bool(self.name_rejected))
        stream.write(bitstream.c_bool(self.is_ftp))
        stream.write(bitstream.c_uint32(self.head_color))
        stream.write(bitstream.c_uint16(0))
        stream.write(bitstream.c_uint32(self.head))
        stream.write(bitstream.c_uint32(self.chest_color))
        stream.write(bitstream.c_uint32(self.chest))
        stream.write(bitstream.c_uint32(self.legs))
        stream.write(bitstream.c_uint32(self.hair_style))
        stream.write(bitstream.c_uint32(self.hair_color))
        stream.write(bitstream.c_uint32(self.left_hand))
        stream.write(bitstream.c_uint32(self.right_hand))
        stream.write(bitstream.c_uint32(self.eyebrows_style))
        stream.write(bitstream.c_uint32(self.eyes_style))
        stream.write(bitstream.c_uint32(self.mouth_style))
        stream.write(bitstream.c_uint32(0))
        stream.write(bitstream.c_uint16(self.last_zone))
        stream.write(bitstream.c_uint16(self.last_map_instance))
        stream.write(bitstream.c_uint32(self.last_map_clone))
        stream.write(bitstream.c_uint64(0))
        stream.write(bitstream.c_uint16(len(self.equipped_items)))
        for item in self.equipped_items:
            stream.write(bitstream.c_uint32(item))

    # For testing just use lot 6010
    @classmethod
    def from_cdclient(cls, lot: int):
        char = LoginCharacter()
        conn = sqlite3.connect("./res/cdclient.sqlite")
        c = conn.cursor()
        c.execute("SELECT displayName FROM Objects WHERE id = ?", (lot,))
        char.current_name = c.fetchone()[0].split("-")[0]
        c.execute("SELECT component_type, component_id FROM ComponentsRegistry WHERE id = ?", (lot,))
        components = c.fetchall()
        for comp in components:
            if comp[0] == 17:
                c.execute("SELECT itemid FROM InventoryComponent WHERE id = ?", (comp[1],))
                items = c.fetchall()
                equipped = []
                for i in items:
                    equipped.append(i[0])
                char.equipped_items = equipped
            elif comp[0] == 35:
                c.execute("SELECT * FROM MinifigComponent WHERE id = ?", (comp[1],))
                minifig_comp = c.fetchone()
                char.head = minifig_comp[1]
                char.chest_color = minifig_comp[6]
                char.legs = minifig_comp[3]
                char.hair_style = minifig_comp[4]
                char.hair_color = minifig_comp[5]
                char.chest = minifig_comp[2]
                char.head_color = minifig_comp[7]
                char.left_hand = minifig_comp[8]
                char.right_hand = minifig_comp[9]
                char.eyebrows_style = minifig_comp[10]
                char.eyes_style = minifig_comp[11]
                char.mouth_style = minifig_comp[12]
        conn.close()
        return char

    def save_to_db(self, account_id, connection):
        c = connection.cursor()
        c.execute("INSERT INTO wlus.character (character_id, current_name, requested_name, head_color,"
                  " head, chest_color, chest, legs, hair_style, hair_color, left_hand, right_hand,"
                  " eyebrow_style, eye_style, mouth_style, account_id) VALUES (%s, %s, %s, %s, %s, %s, %s, "
                  "%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.object_id, self.current_name, self.unapproved_name,
                                                          self.head_color, self.head, self.chest_color, self.chest,
                                                          self.legs, self.hair_style, self.hair_color, self.left_hand,
                                                          self.right_hand, self.eyebrows_style, self.eyes_style,
                                                          self.mouth_style, account_id))
        for i in range(len(self.equipped_items)):
            item_id = LwoObjID.gen_lwoobjid()
            c.execute("INSERT INTO wlus.inventory (object_id, lot, slot, equipped, linked, quantity, player_id)"
                      "VALUES (%s, %s, %s, 1, 1, 1, %s)", (item_id, self.equipped_items[i], i, self.object_id))
        connection.commit()

"""
This file contains all of the replica components and the structs withing them
"""
from pyraknet.bitstream import *
from pyraknet.replicamanager import Replica
from plugins.serializables.packet_enum import ReplicaTypes, SerializedComponents
from plugins.serializables.misc_serializables import Vector3, Vector4
import sqlite3


class ReplicaObject(Replica):

    def __init__(self):
        self.base_data = BaseDataComponent()
        self.components = {}

    def write_construction(self, stream: WriteStream) -> None:
        self.write(stream, ReplicaTypes.CONSTRUCTION.value)

    def serialize(self, stream: WriteStream) -> None:
        self.write(stream, ReplicaTypes.SERIALIZATION.value)

    def write(self, stream: WriteStream, replica_mode) -> None:
        # Not Networked: 12, 31, 35, 36, 45, 55, 56, 64, 65, 68, 73, 104, 113, 114
        self.base_data.replica_mode = replica_mode  # TODO: There has to be a better way to do this
        for comp in self.components:
            self.components[comp].replica_mode = ReplicaTypes.CONSTRUCTION.value
        conn = sqlite3.connect("./res/cdclient.sqlite")
        c = conn.cursor()
        c.execute("SELECT component_type FROM ComponentsRegistry WHERE id = ?", (self.base_data.lot,))
        comp_table = c.fetchall()
        components = []
        for component in comp_table:
            components.append(component[0])
        stream.write(self.base_data)

        if SerializedComponents.POSSESSABLE.value in components:
            pass
        if SerializedComponents.MODULE_ASSEMBLY.value in components:
            pass
        if SerializedComponents.CONTROLLABLE_PHYSICS.value in components:
            stream.write(self.components[SerializedComponents.CONTROLLABLE_PHYSICS.value])
        if SerializedComponents.SIMPLE_PHYSICS.value in components:
            pass
        if SerializedComponents.RIGID_BODY_PHANTOM_PHYSICS.value in components:
            pass
        if SerializedComponents.VEHICLE_PHYSICS.value in components:
            pass
        if SerializedComponents.PHANTOM_PHYSICS.value in components:
            pass
        if SerializedComponents.DESTRUCTIBLE.value in components:
            stream.write(self.components[SerializedComponents.DESTRUCTIBLE.value].destructible_index)
            stream.write(self.components[SerializedComponents.DESTRUCTIBLE.value].stats_index)
        if SerializedComponents.COLLECTIBLE.value in components:
            pass
        if SerializedComponents.PET.value in components:
            pass
        if SerializedComponents.CHARACTER.value in components:
            stream.write(self.components[SerializedComponents.CHARACTER.value])
        if SerializedComponents.INVENTORY.value in components:
            stream.write(self.components[SerializedComponents.INVENTORY.value])
        if SerializedComponents.SCRIPT.value in components:
            pass
        if SerializedComponents.SKILL.value in components:
            stream.write(self.components[SerializedComponents.SKILL.value])
        if SerializedComponents.BASE_COMBAT_AI.value in components:
            pass
        if SerializedComponents.REBUILD.value in components:
            pass
        if SerializedComponents.MOVING_PLATFORM.value in components:
            pass
        if SerializedComponents.SWITCH.value in components:
            pass
        if SerializedComponents.VENDOR.value in components:
            pass
        if SerializedComponents.BOUNCER.value in components:
            pass
        if SerializedComponents.SCRIPTED_ACTIVITY.value in components:
            pass
        if SerializedComponents.RACING_CONTROL.value in components:
            pass
        if SerializedComponents.EXHIBIT.value in components:
            pass
        if SerializedComponents.MODEL.value in components:
            pass
        if SerializedComponents.RENDER.value in components:
            stream.write(self.components[SerializedComponents.RENDER.value])
        if SerializedComponents.COMPONENT_107.value in components:
            stream.write(self.components[SerializedComponents.COMPONENT_107.value])
        if SerializedComponents.MODEL.value in components:
            pass


class BaseDataComponent(Serializable):
    """
    Base Data should be supplied with every replica.
    replica_mode refers to whether or not it is construction, serialization or destruction.
       Construction - 0
       Serialization - 1
       Destruction - 2
    """
    def __init__(self, replica_mode=0):
        self.replica_mode = replica_mode
        self.object_id = 0
        self.lot = 0
        self.name = ""
        self.time_since_created = 0
        self.has_trigger = False
        self.spawner_id = 0
        self.spawner_node_id = 0
        self.scale = 1
        self.object_world_state = -1
        self.gm_level = 0

    def serialize(self, stream: WriteStream) -> None:
        if self.replica_mode == ReplicaTypes.CONSTRUCTION.value:
            stream.write(c_int64(self.object_id))
            stream.write(c_int32(self.lot))
            stream.write(self.name, length_type=c_uint8)
            stream.write(c_uint32(self.time_since_created))
            stream.write(c_bit(False))  # Unimplemented struct
            stream.write(c_bit(self.has_trigger))
            stream.write(c_bit(self.spawner_id != 0))
            if self.spawner_id != 0:
                stream.write(c_int64(self.spawner_id))
            stream.write(c_bit(self.spawner_node_id != 0))
            if self.spawner_node_id != 0:
                stream.write(c_uint32(self.spawner_node_id))
            stream.write(c_bit(self.scale != 1))
            if self.scale != 1:
                stream.write(c_float(self.scale))
            stream.write(c_bit(self.object_world_state != -1))
            if self.object_world_state != -1:
                stream.write(c_uint8(self.object_world_state))
            stream.write(c_bit(self.gm_level != 0))
            if self.gm_level != 0:
                stream.write(c_uint8(self.gm_level))
        stream.write(c_bit(False))  # Unimplemented struct

    @classmethod
    def deserialize(cls, stream: ReadStream) -> Serializable:
        raise Exception("This struct cannot be deserialized")


class ControllablePhysicsComponent(Serializable):

    def __init__(self, replica_mode=0):
        self.replica_mode = replica_mode
        self.jetpack_equipped = False
        self.jetpack_effect = 0
        self.in_air = False
        self.gravity_multiplier = 1
        self.speed_multiplier = 1
        self.position = Vector3()
        self.rotation = Vector4()
        self.on_ground = True
        self.on_rail = False
        self.velocity = Vector3()
        self.angular_velocity = Vector3()

    def serialize(self, stream: WriteStream) -> None:
        if self.replica_mode == ReplicaTypes.CONSTRUCTION.value:
            stream.write(c_bit(self.jetpack_equipped))
            if self.jetpack_equipped:
                stream.write(c_uint32(self.jetpack_effect))
                stream.write(c_bit(self.in_air))
                stream.write(c_bit(False))
            stream.write(c_bit(False))  # Undiscovered struct?
        stream.write(c_bit(self.gravity_multiplier != 1 or self.speed_multiplier != 1))
        if self.gravity_multiplier != 1 or self.speed_multiplier != 1:
            stream.write(c_float(self.gravity_multiplier))
            stream.write(c_float(self.speed_multiplier))
        stream.write(c_bit(False))  # Undiscovered struct?
        stream.write(c_bit(False))  # Undiscovered struct?
        stream.write(c_bit(True))
        stream.write(self.position)
        stream.write(self.rotation)
        stream.write(c_bit(self.on_ground))
        stream.write(c_bit(self.on_rail))
        stream.write(c_bit(self.velocity != Vector3()))
        if self.velocity != Vector3():
            stream.write(self.velocity)
        stream.write(c_bit(self.angular_velocity != Vector3()))
        if self.angular_velocity != Vector3():
            stream.write(self.angular_velocity)
        stream.write(c_bit(False))  # Some struct relating to moving platforms
        if self.replica_mode == ReplicaTypes.SERIALIZATION.value:
            stream.write(c_bit(False))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> Serializable:
        raise Exception("This struct cannot be deserialized")


class DestructibleIndex(Serializable):
    """
    This index is fairly unresearched.
    """
    def __init__(self, replica_mode=0):
        self.replica_mode = replica_mode

    def serialize(self, stream: WriteStream) -> None:
        if self.replica_mode == ReplicaTypes.CONSTRUCTION.value:
            stream.write(c_bit(False))
            stream.write(c_bit(False))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> Serializable:
        raise Exception("This struct cannot be deserialized")


class StatsIndex(Serializable):

    def __init__(self, replica_mode=0):
        self.replica_mode = replica_mode
        self.health = 0
        self.max_health = 0
        self.armor = 0
        self.max_armor = 0
        self.imagination = 0
        self.max_imagination = 0
        self.absorbtion_points = 0
        self.is_gm_immune = False
        self.immune = False
        self.shielded = False
        self.factions = []
        self.is_smashable = False

    def serialize(self, stream: WriteStream) -> None:
        if self.replica_mode == ReplicaTypes.CONSTRUCTION.value:
            stream.write(c_bit(False))
        stream.write(c_bit(True))
        stream.write(c_uint32(self.health))
        stream.write(c_float(self.max_health))
        stream.write(c_uint32(self.armor))
        stream.write(c_float(self.max_armor))
        stream.write(c_uint32(self.imagination))
        stream.write(c_float(self.max_imagination))
        stream.write(c_uint32(self.absorbtion_points))
        stream.write(c_bit(self.immune))
        stream.write(c_bit(self.is_gm_immune))
        stream.write(c_bit(self.shielded))
        stream.write(c_float(self.max_health))
        stream.write(c_float(self.max_armor))
        stream.write(c_float(self.max_imagination))
        stream.write(c_uint32(len(self.factions)))
        for faction in self.factions:
            stream.write(c_int32(faction))
        stream.write(c_bit(self.is_smashable))
        if self.replica_mode == ReplicaTypes.CONSTRUCTION.value:
            stream.write(c_bit(False))
            stream.write(c_bit(False))
            if self.is_smashable:
                stream.write(c_bit(False))
                stream.write(c_bit(False))
        stream.write(c_bit(False))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> Serializable:
        raise Exception("This struct cannot be deserialized")


class CharacterComponent(Serializable):

    def __init__(self, replica_mode=0):
        self.replica_mode = replica_mode
        self.level = 0
        self.hair_color = 0
        self.hair_style = 0
        self.shirt_color = 0
        self.pants_color = 0
        self.eyebrows = 0
        self.eyes = 0
        self.mouth = 0
        self.account_id = 0
        self.lego_score = 0
        self.ftp = False
        self.character_stats = []
        for _ in range(27):
            self.character_stats.append(0)
        self.world_transition_state = 0
        self.ldf_rocket_info = "1:9746;1:9747;1:9748;"
        self.pvp = False
        self.is_gm = False
        self.gm_level = 0
        self.activity = 0
        # TODO: Add guild struct and vehicle struct

    def serialize(self, stream: WriteStream) -> None:
        stream.write(c_bit(False))  # Vehicle struct
        stream.write(c_bit(False))
        # stream.write(c_uint32(self.level))
        stream.write(c_bit(False))
        if self.replica_mode == ReplicaTypes.CONSTRUCTION.value:
            stream.write(c_bit(False))
            stream.write(c_bit(False))
            stream.write(c_bit(False))
            stream.write(c_bit(False))
            stream.write(c_uint32(self.hair_color))
            stream.write(c_uint32(self.hair_style))
            stream.write(c_uint32(0))
            stream.write(c_uint32(self.shirt_color))
            stream.write(c_uint32(self.pants_color))
            stream.write(c_uint32(0))
            stream.write(c_uint32(0))
            stream.write(c_uint32(self.eyebrows))
            stream.write(c_uint32(self.eyes))
            stream.write(c_uint32(self.mouth))
            stream.write(c_uint64(self.account_id))
            stream.write(c_uint64(0))
            stream.write(c_uint64(0))
            stream.write(c_uint64(self.lego_score))
            stream.write(c_bit(self.ftp))
            for stat in self.character_stats:
                stream.write(c_uint64(stat))
            if self.world_transition_state == 1:
                stream.write(c_bit(True))
                stream.write(c_bit(False))
                stream.write(self.ldf_rocket_info, length_type=c_uint16)
            elif self.world_transition_state == 2:
                stream.write(c_bit(False))
                stream.write(c_bit(True))
            else:
                stream.write(c_bit(False))
                stream.write(c_bit(False))
        stream.write(c_bit(True))
        stream.write(c_bit(self.pvp))
        stream.write(c_bit(self.is_gm))
        stream.write(c_uint8(self.gm_level))
        stream.write(c_bit(False))
        stream.write(c_uint8(0))
        stream.write(c_bit(self.activity != 0))
        if self.activity != 0:
            stream.write(c_uint32(self.activity))
        stream.write(c_bit(False))  # Guild struct

    @classmethod
    def deserialize(cls, stream: ReadStream) -> Serializable:
        raise Exception("This struct cannot be deserialized")


class InventoryItem(Serializable):

    def __init__(self):
        self.object_id = 0
        self.lot = 0
        self.count = 1
        self.slot = 0
        self.inventory_type = 4

    def serialize(self, stream: WriteStream) -> None:
        stream.write(c_int64(self.object_id))
        stream.write(c_int32(self.lot))
        stream.write(c_bit(False))
        stream.write(c_bit(True))
        stream.write(c_uint32(self.count))
        stream.write(c_bit(True))
        stream.write(c_uint16(self.slot))
        stream.write(c_bit(True))
        stream.write(c_uint32(self.inventory_type))
        stream.write(c_bit(False))
        stream.write(c_bit(True))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> Serializable:
        raise Exception("This struct cannot be deserialized")


class InventoryComponent(Serializable):

    def __init__(self, replica_mode=0):
        self.replica_mode = replica_mode
        self.items = []

    def serialize(self, stream: WriteStream) -> None:
        stream.write(c_bit(True))
        stream.write(c_uint32(len(self.items)))
        for item in self.items:
            stream.write(item)
        stream.write(c_bit(False))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> Serializable:
        raise Exception("This struct cannot be deserialized")


class SkillComponent(Serializable):
    """
    Not even really sure what this is for
    """
    def __init__(self, replica_mode=0):
        self.replica_mode = replica_mode

    def serialize(self, stream: WriteStream) -> None:
        if self.replica_mode == ReplicaTypes.CONSTRUCTION.value:
            stream.write(c_bit(False))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> Serializable:
        raise Exception("This struct cannot be deserialized")


class RenderComponent(Serializable):
    """
    Not even really sure what this is for
    """
    def __init__(self, replica_mode=0):
        self.replica_mode = replica_mode
        # TODO: I should probably at least implement this struct

    def serialize(self, stream: WriteStream) -> None:
        if self.replica_mode == ReplicaTypes.CONSTRUCTION.value:
            stream.write(c_int32(0))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> Serializable:
        raise Exception("This struct cannot be deserialized")


class Component107(Serializable):

    def __init__(self, replica_mode = 0):
        self.replica_mode = replica_mode

    def serialize(self, stream: WriteStream) -> None:
        stream.write(c_bit(False))

    @classmethod
    def deserialize(cls, stream: ReadStream) -> Serializable:
        raise Exception("This struct cannot be deserialized")


class DestructibleComponent:

    def __int__(self, replica_mode=0):
        self.replica_mode = replica_mode
        self.destructible_index = DestructibleIndex()
        self.stats_index = StatsIndex()





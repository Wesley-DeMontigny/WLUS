"""
This file contains all of the replica components and the structs withing them
"""
from pyraknet import bitstream


class BaseDataComponent(bitstream.Serializable):
    """
    Base Data should be supplied with every replica.
    replica_mode refers to whether or not it is construction, serialization or destruction.
       Construction - 0
       Serialization - 1
       Destruction - 2
    """
    def __init__(self, replica_mode: int = 0):
        self.replica_mode = replica_mode
        self.object_id = 0
        self.lot = 0
        self.name = ""
        self.time_since_created = 0
        self.has_trigger = False
        self.spawner_id = 0
        self.spawner_node_id = 0
        self.scale = 1
        self.object_world_state = 0
        self.gm_level = 0
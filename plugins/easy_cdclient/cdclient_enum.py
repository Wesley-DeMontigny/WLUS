"""
Contains various enum for the cdclient
"""
from enum import IntEnum

zone_checksums = {1200: 0xda1e6b30,
                  1000: 0x20b8087c,
                  1001: 0x26680a3c,
                  1100: 0x49525511,
                  # 1101: 0x538214e2,
                  1102: 0x0fd403da,
                  1150: 0x0fd403da,
                  1151: 0x0a890303,
                  1201: 0x476e1330,
                  # 1203: 0x10fc0502,
                  1204: 0x07d40258,
                  1250: 0x058d0191,
                  1251: 0x094f045d,
                  1300: 0x12eac290,
                  1302: 0x0b7702ef,
                  # 9999: 0x13600646 #Frostburgh
                  # 1303: 0x152e078a,
                  1350: 0x04b6015c,
                  1400: 0x8519760d,
                  1402: 0x02f50187,
                  # 1403: 0x81850f4e,
                  1450: 0x03f00126,
                  1600: 0x07c202ee,
                  1601: 0x02320106,
                  1602: 0x0793037f,
                  1603: 0x043b01ad,
                  1604: 0x181507dd,
                  1700: 0x02040138,
                  1800: 0x4b17a399,
                  1900: 0x9e4af43c,
                  2000: 0x4d692c74,
                  2001: 0x09eb00ef,
                  1124: 0xaa690e20}


class COMPONENTS(IntEnum):
    CONTROLLABLE_PHYSICS = 1
    RENDER = 2
    SIMPLE_PHYSICS = 3
    CHARACTER = 4
    SCRIPT = 5
    BOUNCER = 6
    DESTROYABLE = 7
    SKILL = 9
    SPAWNER = 10
    ITEM = 11
    REBUILD = 12
    REBUILD_START = 13
    VENDOR = 16
    INVENTORY = 17
    PROJECTILE_PHYSICS = 18
    SHOOTING_GALLERY = 19
    RIGID_BODY_PHANTOM_PHYSICS = 20
    CHEST = 22
    COLLECTIBLE = 23
    BLUEPRINT = 24
    MOVING_PLATFORM = 25
    PET = 26
    PLATFORM_BOUNDARY = 27
    MODULE = 28
    ARCADE = 29
    VEHICLE_PHYSICS_0 = 30
    MOVEMENT_AI = 31
    EXHIBIT = 32
    MINIFIG = 35
    PROPERTY = 36
    PET_CREATOR = 37
    MODEL_BUILDER = 38
    SCRIPTED_ACTIVITY = 39
    PHANTOM_PHYSICS = 40
    SPRINGPAD = 41
    B3_BEHAVIORS = 42
    PROPERTY_ENTRANCE = 43
    PROPERTY_MANAGEMENT = 45
    VEHICLE_PHYSICS_1 = 46
    PHYSICS_SYSTEM = 47
    QUICK_BUILD = 48
    SWITCH = 49
    MINIGAME = 50
    CHANGLING = 51
    CHOICE_BUILD = 52
    PACKAGE = 53
    SOUND_REPEATER = 54
    SOUND_AMBIENT_2D = 55
    SOUND_AMBIENT_3D = 56
    PRECONDITION = 57
    CUSTOM_BUILD_ASSEMBLY = 59
    BASE_COMBAT_AI = 60
    MODULE_ASSEMBLY = 61
    SHOWCASE_MODEL_HANDLER = 62
    RACING_MODULE = 63
    GENERIC_ACTIVATOR = 64
    PROPERTY_VENDOR = 65
    HF_LIGHT_DIRECTION_GADGET = 66
    ROCKET_LAUNCH = 67
    ROCKET_LANDING = 68
    RACING_CONTROL = 71
    FACTION_TRIGGER = 72
    MISSION_OFFER = 73
    RACING_STATS = 74
    LUP_EXHIBIT = 75
    SOUND_TRIGGER = 77
    PROXIMITY_MONITOR = 79
    USER_CONTROL = 95
    LUP_LAUNCHPAD = 97
    BRICK_DONATION = 100
    COMMENDATION_VENDOR = 102
    RAIL_ACTIVATOR = 104
    ROLLER = 105
    POSSESSABLE = 108
    PROPERTY_PLAQUE = 113
    BUILD_BORDER = 114
    CULLING_PLANE = 116
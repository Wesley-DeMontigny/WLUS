from messages import Message
from bitstream import *
import socket
from os import getpid
from enum import Enum

class LegoPackets:
    LOGIN_CUTSOM_MSG = 0x05
    LOGIN_SUCCESS = 0x01
    LOGIN_ERROR = 0x00
    LOGIN_WRONG_INFO = 0x06
    LOGIN_BANNED = 0x02


class ReplicaTypes():
    REPLICA_CONSTRUCTION_PACKET = 0
    REPLICA_SERIALIZATION_PACKET = 1
    REPLICA_DESTRUCTION_PACKET = 2

class Zones:
    NO_ZONE = 0
    VENTURE_EXPLORER = 1000
    VENTURE_EXPLORER_RETURN = 1001,
    AVANT_GARDENS = 1100
    AVANT_GARDENS_SURVIVAL = 1101
    SPIDER_QUEEN_BATTLE = 1102
    BLOCK_YARD = 1150
    AVANT_GROVE = 1151
    NIMBUS_STATION = 1200
    PET_COVE = 1201
    VERTIGO_LOOP_RACETRACK = 1203
    BATTLE_OF_NIMBUS_STATION = 1204
    NIMBUS_ROCK = 1250
    NIMBUS_ISLE = 1251
    GNARLED_FOREST = 1300
    CANYON_COVE = 1302
    KEELHAUL_CANYON = 1303
    CHANTEY_SHANTEY = 1350
    FORBIDDEN_VALLEY = 1400
    FORBIDDEN_VALLEY_DRAGON = 1402
    DRAGONMAW_CHASM = 1403
    RAVEN_BLUFF = 1450
    STARBASE_3001 = 1600
    DEEP_FREEZE = 1601
    ROBOT_CITY = 1602
    MOON_BASE = 1603
    PORTABELLO = 1604
    LEGO_CLUB = 1700
    CRUX_PRIME = 1800
    NEXUS_TOWER = 1900
    NINJAGO_MONASTERY = 2000
    FRANKJAW_BATTLE = 2001

    zoneChecksums = {VENTURE_EXPLORER : [0x7c, 0x08, 0xb8, 0x20],
        VENTURE_EXPLORER_RETURN : [0x3c, 0x0a, 0x68, 0x26],
        AVANT_GARDENS : [0x11, 0x55, 0x52, 0x49],
        AVANT_GARDENS_SURVIVAL : [0x11, 0x55, 0x52, 0x49],
        SPIDER_QUEEN_BATTLE : [0xda, 0x03, 0xd4, 0x0f],
        BLOCK_YARD : [0xda, 0x03, 0xd4, 0x0f],
        AVANT_GROVE : [0x03, 0x03, 0x89, 0x0a],
        NIMBUS_STATION : [0x30, 0x6b, 0x1e, 0xda],
        PET_COVE : [0x30, 0x13, 0x6e, 0x47],
        VERTIGO_LOOP_RACETRACK : [0x02, 0x05, 0xfc, 0x10],
        BATTLE_OF_NIMBUS_STATION : [0x58, 0x02, 0xd4, 0x07],
        NIMBUS_ROCK : [0x91, 0x01, 0x8d, 0x05],
        NIMBUS_ISLE : [0x5d, 0x04, 0x4f, 0x09],
        GNARLED_FOREST : [0x90, 0xc2, 0xea, 0x12],
        CANYON_COVE : [0xef, 0x02, 0x77, 0x0b],
        CHANTEY_SHANTEY : [0x5c, 0x01, 0xb6, 0x04],
        FORBIDDEN_VALLEY : [0x0d, 0x76, 0x19, 0x85],
        FORBIDDEN_VALLEY_DRAGON : [0x87, 0x01, 0xf5, 0x02],
        DRAGONMAW_CHASM : [0x4e, 0x0f, 0x85, 0x81],
        RAVEN_BLUFF : [0x26, 0x01, 0xf0, 0x03],
        STARBASE_3001 : [0xee, 0x02, 0xc2, 0x07],
        DEEP_FREEZE : [0x06, 0x01, 0x32, 0x02],
        ROBOT_CITY : [0x7f, 0x03, 0x93, 0x07],
        MOON_BASE : [0xad, 0x01, 0x3b, 0x04],
        PORTABELLO : [0xdd, 0x07, 0x15, 0x18],
        LEGO_CLUB : [0x38, 0x01, 0x04, 0x02],
        CRUX_PRIME : [0x99, 0xa3, 0x17, 0x4b],
        NEXUS_TOWER : [0x3c, 0xf4, 0x4a, 0x9e],
        NINJAGO_MONASTERY : [0x74, 0x2c, 0x69, 0x4d],
        FRANKJAW_BATTLE : [0xef, 0x00, 0xeb, 0x09]}

    defaultZoneSpawns = {VENTURE_EXPLORER : [-627.1862, 613.326233, -47.2231674],
        VENTURE_EXPLORER_RETURN : [-187.2391, 608.2743, 54.5554352],
        AVANT_GARDENS : [522.9949, 406.040375, 129.992722],
        AVANT_GARDENS_SURVIVAL : [35.0297, 365.780426, -201.578369],
        SPIDER_QUEEN_BATTLE : [-18.7062054, 440.20932, 37.5326424],
        BLOCK_YARD : [-18.7062054, 440.20932, 37.5326424],
        AVANT_GROVE : [25.0526543, 472.215027, -24.318882],
        NIMBUS_STATION : [-40.0, 293.047, -16.0],
        PET_COVE : [111.670906, 229.282776, 179.87793],
        VERTIGO_LOOP_RACETRACK : [0.0, 0.0, 0.0],
        BATTLE_OF_NIMBUS_STATION : [-12.1019106, 212.900024, 191.147964],
        NIMBUS_ROCK : [-17.8299046, 440.509674, 30.0326862],
        NIMBUS_ISLE : [31.55009, 470.885254, 193.457321],
        GNARLED_FOREST : [-329.965881, 302.470184, -470.232758],
        CANYON_COVE : [-293.072571, 233.0, -4.16148],
        CHANTEY_SHANTEY : [-19.713892, 440.20932, 26.935009],
        FORBIDDEN_VALLEY : [390.284363, 229.452881, -511.350983],
        FORBIDDEN_VALLEY_DRAGON : [-264.426575, 290.3452, 308.619049],
        DRAGONMAW_CHASM : [-1457.71826, 794.0, -332.2917],
        RAVEN_BLUFF : [-26.8431015, 425.11496, 53.7349777],
        STARBASE_3001 : [34.6352119, 1571.29309, 48.0321465],
        DEEP_FREEZE : [-90.30964, 211.087067, -126.3196],
        ROBOT_CITY : [-163.2, 217.254913, 172.0],
        MOON_BASE : [9.18036652, 48.79997, 109.610374],
        PORTABELLO : [-99.80103, 231.916946, -162.67955],
        LEGO_CLUB : [-359.979156, 1066.328, -369.287781],
        CRUX_PRIME : [-241.965515, 92.78052, 557.327942],
        NEXUS_TOWER : [165.355682, 1164.17822, -543.9093],
        NINJAGO_MONASTERY : [-446.79715, 171.158859, 1122.83545],
        FRANKJAW_BATTLE : [11.26009, 211.05188, 40.6721039]}


class Creation_Lots:
    #Shirts
    SHIRT_BRIGHT_RED = 4049
    SHIRT_BRIGHT_BLUE = 4083
    SHIRT_BRIGHT_YELLOW = 4117
    SHIRT_DARK_GREEN = 4151
    SHIRT_BRIGHT_ORANGE = 4185
    SHIRT_BLACK = 4219
    SHIRT_DARK_STONE_GRAY = 4253
    SHIRT_MEDIUM_STONE_GRAY = 4287
    SHIRT_REDDISH_BROWN = 4321
    SHIRT_WHITE = 4355
    SHIRT_MEDIUM_BLUE = 4389
    SHIRT_DARK_RED = 4423
    SHIRT_EARTH_BLUE = 4457
    SHIRT_EARTH_GREEN = 4491
    SHIRT_BRICK_YELLOW = 4525
    SHIRT_SAND_BLUE = 4559
    SHIRT_SAND_GREEN = 4593
    #Pants
    PANTS_BRIGHT_RED = 2508
    PANTS_BRIGHT_ORANGE = 2509
    PANTS_BRICK_YELLOW = 2511
    PANTS_MEDIUM_BLUE = 2513
    PANTS_SAND_GREEN = 2514
    PANTS_DARK_GREEN = 2515
    PANTS_EARTH_GREEN = 2516
    PANTS_EARTH_BLUE = 2517
    PANTS_BRIGHT_BLUE = 2519
    PANTS_SAND_BLUE = 2520
    PANTS_DARK_STONE_GRAY = 2521
    PANTS_MEDIUM_STONE_GRAY = 2522
    PANTS_WHITE = 2523
    PANTS_BLACK = 2524
    PANTS_REDDISH_BROWN = 2526
    PANTS_DARK_RED = 2527

#Returns a shirtColor and shirtStyle with a corresponding item
def getShirtID(shirtColor, shirtStyle):
    shirtID = 0

    if(shirtColor == 0):
        if(shirtStyle >= 35):
            shirtID = 5730
        else:
            shirtID = Creation_Lots.SHIRT_BRIGHT_RED
    elif(shirtColor == 1):
        if(shirtStyle >= 35):
            shirtID = 5736
        else:
            shirtID = Creation_Lots.SHIRT_BRIGHT_BLUE
    elif (shirtColor == 3):
        if(shirtStyle >= 35):
            shirtID = 5808
        else:
            shirtID = Creation_Lots.SHIRT_DARK_GREEN
    elif (shirtColor == 5):
        if(shirtStyle >= 35):
            shirtID = 5754
        else:
            shirtID = Creation_Lots.SHIRT_BRIGHT_ORANGE
    elif (shirtColor == 6):
        if(shirtStyle >= 35):
            shirtID = 5760
        else:
            shirtID = Creation_Lots.SHIRT_BLACK
    elif (shirtColor == 7):
        if(shirtStyle >= 35):
            shirtID = 5766
        else:
            shirtID = Creation_Lots.SHIRT_DARK_STONE_GRAY
    elif (shirtColor == 8):
        if(shirtStyle >= 35):
            shirtID = 5772
        else:
            shirtID = Creation_Lots.SHIRT_MEDIUM_STONE_GRAY
    elif (shirtColor == 9):
        if(shirtStyle >= 35):
            shirtID = 5778
        else:
            shirtID = Creation_Lots.SHIRT_REDDISH_BROWN
    elif (shirtColor == 10):
        if(shirtStyle >= 35):
            shirtID = 5784
        else:
            shirtID = Creation_Lots.SHIRT_WHITE
    elif (shirtColor == 11):
        if(shirtStyle >= 35):
            shirtID = 5802
        else:
            shirtID = Creation_Lots.SHIRT_MEDIUM_BLUE
    elif (shirtColor == 13):
        if(shirtStyle >= 35):
            shirtID = 5796
        else:
            shirtID = Creation_Lots.SHIRT_DARK_RED
    elif (shirtColor == 14):
        if(shirtStyle >= 35):
            shirtID = 5802
        else:
            shirtID = Creation_Lots.SHIRT_EARTH_BLUE
    elif (shirtColor == 15):
        if(shirtStyle >= 35):
            shirtID = 5808
        else:
            shirtID = Creation_Lots.SHIRT_EARTH_GREEN
    elif (shirtColor == 16):
        if(shirtStyle >= 35):
            shirtID = 5814
        else:
            shirtID = Creation_Lots.SHIRT_BRICK_YELLOW
    elif (shirtColor == 84):
        if(shirtStyle >= 35):
            shirtID = 5820
        else:
            shirtID = Creation_Lots.SHIRT_SAND_BLUE
    elif (shirtColor == 96):
        if(shirtStyle >= 35):
            shirtID = 5826
        else:
            shirtID = Creation_Lots.SHIRT_SAND_GREEN

    editedShirtColor = shirtID

    finalShirtID = None

    if(shirtStyle >= 35):
        finalShirtID = editedShirtColor + (shirtStyle - 35)
    else:
        finalShirtID = editedShirtColor + (shirtStyle - 1)

    return finalShirtID

#Just returns all the different pants colors with corresponding items
def getPantsID(pantsColor):
    if(pantsColor == 0):
        return Creation_Lots.PANTS_BRIGHT_RED
    elif(pantsColor == 1):
        return Creation_Lots.PANTS_BRIGHT_BLUE
    elif(pantsColor == 3):
        return Creation_Lots.PANTS_DARK_GREEN
    elif(pantsColor == 5):
        return Creation_Lots.PANTS_BRIGHT_ORANGE
    elif(pantsColor == 6):
        return Creation_Lots.PANTS_BLACK
    elif(pantsColor == 7):
        return Creation_Lots.PANTS_DARK_STONE_GRAY
    elif(pantsColor == 8):
        return Creation_Lots.PANTS_MEDIUM_STONE_GRAY
    elif(pantsColor == 9):
        return Creation_Lots.PANTS_REDDISH_BROWN
    elif(pantsColor == 10):
        return Creation_Lots.PANTS_WHITE
    elif(pantsColor == 11):
        return Creation_Lots.PANTS_MEDIUM_BLUE
    elif(pantsColor == 13):
        return Creation_Lots.PANTS_DARK_RED
    elif(pantsColor == 14):
        return Creation_Lots.PANTS_EARTH_BLUE
    elif(pantsColor == 15):
        return Creation_Lots.PANTS_EARTH_GREEN
    elif(pantsColor == 16):
        return Creation_Lots.PANTS_BRICK_YELLOW
    elif(pantsColor == 84):
        return Creation_Lots.PANTS_SAND_BLUE
    elif(pantsColor == 96):
        return Creation_Lots.PANTS_SAND_GREEN
    else:
        return 2508
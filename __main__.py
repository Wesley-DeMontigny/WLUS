import os
import threading
from threading import Thread
import asyncio
from messages import Message
import server
from bitstream import *
from socket import *
from Packet import *
from reliability import PacketReliability
import uuid
from replicamanager import *
from DBHandlers import *
from time import sleep
from GameMessage import *
from LDFReader import *
from ReplicaPacket import *
from World import WorldServer
from Auth import AuthServer

if __name__ == "__main__":
	DBServerStarup()

	WorldServer(("127.0.0.1", 2002), max_connections=10, incoming_password=b"3.25 ND1", role="WORLD")
	AuthServer(("127.0.0.1", 1001), max_connections=10, incoming_password=b"3.25 ND1", role="AUTH")

	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()

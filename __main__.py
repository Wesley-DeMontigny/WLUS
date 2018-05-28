import AuthServer
from GameManager import *
import asyncio
import WorldServer
import pickle
import threading
from pathlib import Path
import os
import time
import sqlite3
from GameDB import GameDB
import pyraknet

def pickleGame(GM):
	pickledFile = open(os.getcwd() + "/Game.pickle", "wb")
	pickle.dump(GM, pickledFile, pickle.HIGHEST_PROTOCOL)

def saveGame(GM):
	while True:
		pickleGame(GM)
		print("Game Was Autosaved")
		time.sleep(30)

if __name__ == "__main__":

	pickledGame = Path(os.getcwd() + "/Game.pickle")
	GM = None
	if(pickledGame.exists() != True):
		GM = GameManager()

		GM.registerAccount("wesley", "play")

		pickleGame(GM)
	else:
		print("Loaded Pickled Game")
		pickledFile = open(pickledGame, "rb")
		GM = pickle.load(pickledFile)
		GM.purgePlayers()
		GM.clearSessions()

	pickleThread = threading.Thread(target=saveGame, args=[GM,])
	pickleThread.start()

	CDClientDB : GameDB = GameDB(sqlite3.connect("resources/cdclient.sqlite", check_same_thread=False))
	Auth = AuthServer.AuthServer(("localhost", 1001), max_connections=10, incoming_password=b"3.25 ND1", GameManager=GM, CDClient=CDClientDB)
	World = WorldServer.WorldServer(("localhost", 2002), max_connections=10, incoming_password=b"3.25 ND1", GameManager=GM, CDClient=CDClientDB)

	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()
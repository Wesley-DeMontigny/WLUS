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
from copy import deepcopy
from GameDB import GameDB
from AccountManager import AccountManager

def serializeObject(Object : any, Filename : str):
	pickledFile = open(os.getcwd() + "/" + Filename, "wb")
	pickle.dump(GM, pickledFile, pickle.HIGHEST_PROTOCOL)

def save(GM, ServerDB):
	while True:
		time.sleep(5)
		adjGM = deepcopy(GM)
		adjGM.AccountManager = None
		adjGM.purgePlayers()
		adjGM.Sessions = []
		serializeObject(adjGM, "Game.pickle")
		GM.AccountManager.Save(GM, ServerDB)


if __name__ == "__main__":

	pickledGame = Path(os.getcwd() + "/Game.pickle")
	GM = None
	if(pickledGame.exists() != True):
		GM = GameManager()

		serializeObject(GM, "Game.pickle")
		print("Created and Serialized Game Manager")
	else:
		print("Loaded Pickled Game File")
		pickledFile = open(pickledGame, "rb")
		GM = pickle.load(pickledFile)
		GM.purgePlayers()
		GM.Sessions = []

	CDClientDB : GameDB = GameDB(sqlite3.connect("resources/cdclient.sqlite", check_same_thread=False))
	ServerDB : GameDB = GameDB(sqlite3.connect("server.sqlite", check_same_thread=False))

	GM.AccountManager = AccountManager()
	GM.AccountManager.InitializeAccounts(ServerDB)
	pickleThread = threading.Thread(target=save, args=[GM, ServerDB])
	pickleThread.start()

	serverIP = "127.0.0.1"

	Auth = AuthServer.AuthServer((serverIP, 1001), max_connections=10, incoming_password=b"3.25 ND1", GameManager=GM, CDClient=CDClientDB, ServerDB=ServerDB)
	World = WorldServer.WorldServer((serverIP, 2002), max_connections=10, incoming_password=b"3.25 ND1", GameManager=GM, CDClient=CDClientDB, ServerDB=ServerDB)

	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()
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
from AccountManager import AccountManager

def serializeObject(Object : any, Filename : str):
	pickledFile = open(os.getcwd() + "/" + Filename, "wb")
	pickle.dump(GM, pickledFile, pickle.HIGHEST_PROTOCOL)

def save(GM, Accounts):
	while True:
		serializeObject(GM, "Game.pickle")
		#print("Game Was Autosaved")
		serializeObject(Accounts, "Accounts.pickle")
		#print("Accounts Were Autosaved")
		time.sleep(15)


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
		GM.clearSessions()

	pickledAccounts = Path(os.getcwd() + "/Accounts.pickle")
	Accounts = None
	if(pickledAccounts.exists() != True):
		Accounts = AccountManager()

		Accounts.registerAccount("wesley", "play")

		serializeObject(Accounts, "Accounts.pickle")
		print("Created and Serialized Account Manager")
	else:
		print("Loaded Pickled Accounts File")
		pickledFile = open(pickledAccounts, "rb")
		Accounts = pickle.load(pickledFile)

	GM.AccountManager = Accounts

	pickleThread = threading.Thread(target=save, args=[GM,Accounts])
	pickleThread.start()


	CDClientDB : GameDB = GameDB(sqlite3.connect("resources/cdclient.sqlite", check_same_thread=False))
	Auth = AuthServer.AuthServer(("localhost", 1001), max_connections=10, incoming_password=b"3.25 ND1", GameManager=GM, CDClient=CDClientDB)
	World = WorldServer.WorldServer(("localhost", 2002), max_connections=10, incoming_password=b"3.25 ND1", GameManager=GM, CDClient=CDClientDB)

	loop = asyncio.get_event_loop()
	loop.run_forever()
	loop.close()
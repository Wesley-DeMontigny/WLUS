import pyraknet.server
import sqlite3
from typing import Callable, Any
from enum import IntEnum
from pyraknet.messages import Address
import re

class World():
	def __init__(self, zoneID : int, LUZ : str):
		self.zoneID : int = zoneID
		self.LUZ : str = LUZ

class GameObject():
	def __init__(self, ObjectID, LOT):
		self.ObjectID : int = ObjectID
		self.LOT : int = LOT
		self.Tag : str = None
		self.ReplicaComponents : list = []
		self.onInteraction : Callable = None

class SessionState(IntEnum):
	LoggingIn = 0
	CharacterScreen = 1
	InGame = 3

class Session():
	def __init__(self):
		self.world : World = None
		self.character : Character = None
		self.userKey : str = None
		self.accountUsername : str = None
		self.address : Address = None
		self.accountID : int = None
		self.isAdmin : bool = False
		self.State : SessionState = None

class Character():
	def __init__(self):
		self.gameObject : GameObject = None
		self.accountID : int = None

class DBTable():
	def __init__(self, Name : str, Connection : sqlite3.Connection):
		self.Name : str = Name
		self.Connection : sqlite3.Connection = Connection
	def select(self, Fields : list, Condition : str):
		queryString = "SELECT"
		for i in range(len(Fields)):
			if(i != (len(Fields) -1)):
				queryString += " " + Fields[i] + ","
			else:
				queryString += " " + Fields[i]
		queryString += " FROM " + self.Name
		if(Condition != None):
			queryString += " WHERE " + Condition
		c = self.Connection.cursor()
		query = c.execute(queryString)
		result = query.fetchall()
		rows = []
		for i in range(len(result)):
			dictionary = {}
			for x in range(len(result[i])):
				dictionary[Fields[x]] = result[i][x]
			rows.append(dictionary)
		return rows
	def selectAll(self, Condition : str):
		queryString = "SELECT * FROM " + self.Name
		if(Condition != None):
			queryString += " WHERE " + Condition
		c = self.Connection.cursor()
		query = c.execute(queryString)
		result = query.fetchall()
		rows = []
		fieldQuery = c.execute("SELECT sql FROM sqlite_master WHERE name = '{}'".format(self.Name))
		fieldResult = fieldQuery.fetchone()[0]
		Fields = re.findall(r'`(.*?)`', fieldResult)
		for i in range(len(result)):
			dictionary = {}
			for x in range(len(result[i])):
				dictionary[Fields[x]] = result[i][x]
			rows.append(dictionary)
		return rows
	def insert(self, Values : dict):
		queryString = "INSERT INTO " + self.Name + " ("
		keys = list(Values.keys())
		for i in range(len(keys)):
			if(i != (len(keys) -1)):
				queryString += keys[i] + ","
			else:
				queryString += keys[i] + ")"
		queryString += " VALUES ("
		for x in range(len(keys)):
			if (x != (len(keys) - 1)):
				queryString += Values[keys[x]] + ","
			else:
				queryString += Values[keys[x]] + ")"
		c = self.Connection.cursor()
		c.execute(queryString)
		self.Connection.commit()

class GameDB():
	def __init__(self, Connection : sqlite3.Connection):
		self.connection : sqlite3.Connection = Connection
		c = self.connection.cursor()
		tableList = c.execute("SELECT name FROM sqlite_master")
		self.Tables : dict = {}
		for table in tableList:
			self.Tables[table[0]] = DBTable(table[0], self.connection)

class GameManager():
	def __init__(self):
		self.activeServers : dict = {}
		self.activeSessions : list = []
		self.CDClientDB : GameDB = GameDB(sqlite3.connect("cdclient.sqlite", check_same_thread=False))
		self.ServerDB : GameDB = GameDB(sqlite3.connect("server.sqlite", check_same_thread=False))

	def registerServer(self, ServerName : str, Server : pyraknet.server.Server):
		self.activeServers[ServerName] = Server

	def unregisterServer(self, ServerName : str):
		del self.activeServers[ServerName]

	def registerSession(self, Session : Session):
		self.activeSessions.append(Session)

	def getSessionByAddress(self, address):
		for session in self.activeSessions:
			if(session.address == address):
				return session
		return None

	def getSessionByCharacterID(self, characterID):
		for session in self.activeSessions:
			if(session.character.objectID == characterID):
				return session
		return None

	def getSessionByUsername(self, username):
		for session in self.activeSessions:
			if(session.accountUsername == username):
				return session
		return None
import sqlite3
from Packet import *
from random import randint
from passlib.hash import sha256_crypt


def DBServerStarup():
	conn = sqlite3.connect("server.sqlite")
	c = conn.cursor()
	c.execute("DELETE FROM CurrentSessions")
	c.execute("DELETE FROM World_Objects WHERE LOT = 1")
	c.execute("DELETE FROM Worlds")
	conn.commit()
	conn.close()
	print("Reset Sessions Table")

class databaseManager():
	def __init__(self):
		self.serverConn = sqlite3.connect("server.sqlite", check_same_thread=False)
		self.cdConn = sqlite3.connect("cdclient.sqlite", check_same_thread=False)

	def getLoginResponse(self, username, password):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT Banned, Password FROM Accounts WHERE Username = '"+str(username)+"'")
		q = c.fetchone()
		if(q != None and q[0] != 1 and sha256_crypt.verify(password, q[1])):

			return LegoPackets.LOGIN_SUCCESS
		elif(q == None and not sha256_crypt.verify(q[1], password)):

			return LegoPackets.LOGIN_WRONG_INFO
		else:

			return LegoPackets.LOGIN_BANNED

	def registerAccount(self, username, password):
		crypted_pass = sha256_crypt.encrypt(password)
		conn = self.serverConn
		c = conn.cursor()
		c.execute("INSERT INTO Accounts (Username, Password, Banned, IsAdmin) VALUES ('"+str(username)+"', '"+str(crypted_pass)+"', 0, 0)")
		try:
			conn.commit()
		except:
			pass

	def getAccountByUsername(self, username):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM Accounts WHERE Username = '"+str(username)+"'")
		q = c.fetchone()

		return q

	def getAccountByAccountID(self, account):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM Accounts WHERE ID = '"+str(account)+"'")
		q = c.fetchone()

		return q

	def serverQuery(self, q):
		conn = self.serverConn
		c = conn.cursor()
		returnVal = c.execute(q)
		try:
			conn.commit()
		except:
			pass

		return returnVal


	#State is either 0 (Still Loading In), 1 (In character selection) or 2 (In game)

	def getPlayerNameFromConnection(self, ip, port):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT CharID FROM CurrentSessions WHERE IPAddress = '"+str(ip)+"' AND Port = " + str(port))
		id = c.fetchone()
		c.execute("SELECT Name FROM Characters WHERE ObjectID = " + str(id[0]))
		name = c.fetchone()

		return name

	def getZoneOfObject(self, objectID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT Zone FROM World_Objects WHERE ObjectID = "+str(objectID))
		zone = c.fetchone()

		return zone

	def getObjectIDFromName(self, Name):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT ObjectID FROM Characters WHERE Name = '"+str(Name)+"'")
		q = c.fetchone()

		return q

	def getComponentsForLOT(self, LOT):
		conn = self.cdConn
		c = conn.cursor()
		c.execute("SELECT component_type FROM ComponentsRegistry WHERE id = " + str(LOT))
		q = c.fetchall()
		return q

	def getConnectionsInZone(self, zoneID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT IPAddress, Port FROM CurrentSessions WHERE ZoneID = "+str(zoneID))
		connections = c.fetchall()

		return connections

	def registerSession(self, address, userkey, accountID, state, Port):
		conn = self.serverConn
		c = conn.cursor()
		if(self.getSessionByAccountID(accountID) == None):
			c.execute("INSERT INTO CurrentSessions (AccountID, IPAddress, UserKey, charID, zoneID, State, Port) VALUES ("+str(accountID)+", '"+str(address)+"', '"+str(userkey)+"', NULL, NULL, "+str(state)+", "+str(Port)+")")
		try:
			conn.commit()
		except:
			pass

		print("Registered Session")

	def getSessionByUserKey(self, userKey):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM CurrentSessions WHERE UserKey = '"+str(userKey)+"'")
		q = c.fetchone()

		return q

	def getApplicableMission(self, player, offerer):
		conn = self.cdConn
		c = conn.cursor()
		completed = self.getCompletedMissions(player)
		c.execute("SELECT id, prereqMissionID FROM Missions WHERE offer_objectID = "+str(offerer))
		missions = c.fetchall()
		completedMissions = []
		for mission in completed:
			completedMissions.append(int(mission[0]))
		for mission in missions:
			display = True
			required = str(mission[1]).split("|")
			for neededMission in required:
				if(int(neededMission) not in completedMissions):
					display = False
			if(display == True):
				return int(mission[0])
		return None

	def destroySessionWithUserKey(self, userKey):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("DELETE FROM CurrentSessions WHERE UserKey = '"+str(userKey)+"'")
		try:
			conn.commit()
		except:
			pass

		print("Destroyed Session")

	def destroySessionWithAddress(self, address):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("DELETE FROM CurrentSessions WHERE IPAddress = '"+str(address)+"'")
		try:
			conn.commit()
		except:
			pass

		print("Destroyed Session")

	def registerOrJoinWorld(self, zoneID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM Worlds WHERE Zone = '" + str(zoneID) + "'")
		if(c.fetchone() == None):
			c.execute("INSERT INTO Worlds (Zone, OwnerID, Name) VALUES ("+str(zoneID)+", NULL, NULL)")


	def updateCharacterZone(self, zoneID, characterID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT AccountID FROM Characters WHERE ObjectID = " + str(characterID))
		accountID = c.fetchone()
		c.execute("UPDATE CurrentSessions SET charID = "+str(characterID)+", zoneID = "+str(zoneID)+" WHERE AccountID = " + str(accountID[0]))
		c.execute("UPDATE Characters SET LastZone = " + str(zoneID) + " WHERE AccountID = " + str(accountID[0]) + " AND ObjectID = " + str(characterID))
		try:
			conn.commit()
		except:
			pass


	def setCharacterPos(self, charID, x, y, z):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("UPDATE Characters SET XPos = "+str(x)+", YPos = "+str(y)+", ZPos = "+str(z)+" WHERE ObjectID = "+str(charID))
		try:
			conn.commit()
		except:
			pass


	def getEquippedItems(self, charID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT Object FROM Inventory WHERE Owner = "+str(charID)+" AND Equipped = 1")
		equipped = c.fetchall()

		return equipped

	def getCharacterItems(self, charID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT Object FROM Inventory WHERE Owner = "+str(charID))
		items = c.fetchall()

		return items

	def getCompletedMissions(self, charID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT MissionID FROM CompletedMissions WHERE CharID = " + str(charID))
		missions = c.fetchall()

		return missions

	def getItemInfo(self, objID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT Quantity, Slot FROM Inventory WHERE Object = " + str(objID))
		info = c.fetchone()

		return info

	def getInventoryInfo(self, charID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT Object, Quantity, Slot, Linked, SpawnerID FROM Inventory WHERE Owner = " + str(charID))
		items = c.fetchall()
		LOT = []
		SLOT = []
		OBJECT = []
		QUANTITY = []
		SPAWNERID = []
		LINKED = []
		for item in items:
			c.execute("SELECT LOT FROM Objects WHERE ObjectID = "+str(item[0]))
			object = c.fetchone()
			LOT.append(object)
			OBJECT.append(item[0])
			SLOT.append(item[2])
			QUANTITY.append(item[1])
			SPAWNERID.append(item[4])
			LINKED.append(item[3])

		return LOT, OBJECT, QUANTITY, LINKED, SPAWNERID, SLOT

	def getLOTFromObject(self, objectID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT LOT FROM Objects WHERE ObjectID = "+str(objectID))
		item = c.fetchone()

		return item

	def getSessionByAccountID(self, accountID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM CurrentSessions WHERE AccountID = '"+str(accountID)+"'")
		q = c.fetchone()

		return q

	def deleteCharacter(self, objID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("DELETE FROM Characters WHERE ObjectID = "+str(objID))
		c.execute("DELETE FROM Inventory WHERE Owner = " + str(objID))
		try:
			conn.commit()
		except:
			pass

		print("Deleted Character")

	def getCharacterDataByID(self, charID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM Characters WHERE ObjectID = '"+str(charID)+"'")
		q = c.fetchone()

		return q


	def getCharacterData(self, accountID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM Characters WHERE AccountID = '"+str(accountID)+"'")
		q = c.fetchall()

		return len(q), q

	def findOpenInventorySlot(self, charID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT BackpackSpace FROM Characters WHERE ObjectID = "+str(charID))
		backpack = c.fetchone()
		openSlots = []
		for i in range(backpack[0]):
			openSlots.append(i)
		c.execute("SELECT Slot FROM Inventory WHERE Owner = "+str(charID))
		takenSlots = c.fetchall()
		for row in takenSlots:
			openSlots.remove(row[0])

		if(openSlots == []):
			return None
		return openSlots[0]

	def addItemsToInventory(self, charID, LOT, Quantity, slot=None, Linked=0, Equipped=0):
		conn = self.serverConn
		c = conn.cursor()
		itemSlot = 0
		if(slot != None):
			itemSlot = slot
		else:
			itemSlot = self.findOpenInventorySlot(charID)
			if(itemSlot == None):
				return "Inventory Full"
		object = self.createObject(LOT)
		c.execute("INSERT INTO Inventory (Owner, Object, Quantity, Slot, Linked, Equipped) VALUES ("+str(charID)+", "+str(object)+", "+str(Quantity)+", "+str(itemSlot)+", "+str(Linked)+", "+str(Equipped)+")")
		try:
			conn.commit()
		except:
			pass


	def createObject(self, LOT):
		conn = self.serverConn
		objID = str(randint(100000000000000000, 999999999999999999))
		c = conn.cursor()
		c.execute("INSERT INTO Objects (ObjectID, LOT, SpawnID) VALUES ("+str(objID)+", "+str(LOT)+", NULL)")
		try:
			conn.commit()
		except:
			pass

		return objID

	def createMinifigure(self, AccountID, Name, ShirtColor, ShirtStyle, PantsColor, HairStyle, HairColor, lh, rh, Eyebrows, Eyes, Mouth):
		conn = self.serverConn
		objID = str(randint(100000000000000000,999999999999999999))
		username = Name
		if(Name == ""):
			username = objID
		c = conn.cursor()
		c.execute("INSERT INTO Characters (AccountID, Name, ObjectID, ShirtColor, ShirtStyle, PantsColor, HairStyle, HairColor, lh, rh, Eyebrows, Eyes, Mouth, LastZone, MapInstance, MapClone, Level, Currency, isAlive, UScore, BackpackSpace, MaxHealth, Health, MaxArmor, Armor, MaxImagination, Imagination) VALUES ("+str(AccountID)+", '"+str(username)+"', "+str(objID)+", "+str(ShirtColor)+", "+str(ShirtStyle)+", "+str(PantsColor)+", "+str(HairStyle)+", "+str(HairColor)+", "+str(lh)+", "+str(rh)+", "+str(Eyebrows)+", "+str(Eyes)+", "+str(Mouth)+", 0, 0, 0, 1, 0, 1, 0, 20, 4, 4, 0, 0, 0, 0)")
		try:
			conn.commit()
		except:
			pass

		pantsObj = self.createObject(getPantsID(int(PantsColor)))
		shirtObj = self.createObject(getShirtID(int(ShirtColor), int(ShirtStyle)))
		self.addItemsToInventory(objID, pantsObj, 1, slot=2, Linked=1, Equipped=1)
		self.addItemsToInventory(objID, shirtObj, 1, slot=1, Linked=1, Equipped=1)
		print("Created Minifigure " + username)

	def getSessionBySessionID(self, sessionID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM CurrentSessions WHERE SessionID = '"+str(sessionID)+"'")
		q = c.fetchone()

		return q

	def getSessionByAddress(self, address):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM CurrentSessions WHERE IPAddress = '"+str(address)+"'")
		q = c.fetchone()

		return q

	def getSessionByCharacter(self, objectID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM CurrentSessions WHERE CharID = '"+str(objectID)+"'")
		q = c.fetchone()

		return q

	def getSessionByPlayerName(self, name):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT ObjectID FROM Characters WHERE Name = '"+str(name)+"'")
		id = c.fetchone()

		return self.getSessionByCharacter(id[0])

	def updateSessionByUserKey(self, userkey, state, zoneID, charID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("UPDATE CurrentSessions SET charID = "+str(charID)+", zoneID = "+str(zoneID)+", State = "+str(state)+" WHERE UserKey = '"+str(userkey)+"'")
		try:
			conn.commit()
		except:
			pass


	def updateSessionByAccountID(self, accountID, state, zoneID, charID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("UPDATE CurrentSessions SET charID = "+str(charID)+", zoneID = "+str(zoneID)+", State = "+str(state)+" WHERE AccountID = "+str(accountID))
		try:
			conn.commit()
		except:
			pass


	def registerWorldObject(self, Name, LOT, ObjectID, Zone, posX, posY, posZ, rotX, rotY, rotZ, rotW, networkID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute(
			"INSERT INTO World_Objects (Name, LOT, ObjectID, Zone, posX, posY, posZ, rotX, rotY, rotZ, rotw, NetworkID) VALUES ('"+str(Name)+"', "+str(LOT)+", "+str(ObjectID)+", "+str(Zone)+", "+str(posX)+", "+str(posY)+", "+str(posZ)+", "+str(rotX)+", "+str(rotY)+", "+str(rotZ)+", "+str(rotW)+", "+str(networkID)+")")
		try:
			conn.commit()
		except:
			pass


	def getCharactersInGame(self):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT Name, ObjectID FROM World_Objects WHERE LOT = 1")
		players = c.fetchall()

		return players

	def deleteWorldObject(self, ObjectID):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("DELETE FROM World_Objects WHERE ObjectID = " + str(ObjectID))
		try:
			conn.commit()
		except:
			pass


	def getObjectsInZone(self, Zone):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("SELECT * FROM World_Objects WHERE Zone = " + str(Zone))
		objects = c.fetchall()

		return objects

	def getObjectType(self, LOT):
		conn = self.cdConn
		c = conn.cursor()
		c.execute("SELECT type FROM Objects WHERE id = " + str(LOT))
		q = c.fetchone()

		return q

	def updateWorldObject(self, ObjectID, posX, posY, posZ, rotX, rotY, rotZ, rotW):
		conn = self.serverConn
		c = conn.cursor()
		c.execute("UPDATE World_Objects SET posX = " + str(posX) + ", posY = " + str(posY) + ", posZ = " + str(posZ) + ", rotX = " + str(rotX) + ", rotY = " + str(rotY) + ", rotZ = " + str(rotZ) + ", rotW = " + str(rotW) +  " WHERE ObjectID = " + str(ObjectID))
		try:
			conn.commit()
		except:
			pass

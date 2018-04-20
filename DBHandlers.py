import sqlite3
from Packet import *
from random import randint

def getLoginResponse(username, password):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT Banned FROM Accounts WHERE Username = '"+username+"' AND Password = '"+password+"'")
    q = c.fetchone()
    print("SELECT Banned FROM Accounts WHERE Username = '"+username+"' AND Password = '"+password+"'")
    if(q != None and q[0] != 1):
        conn.commit()
        conn.close()
        return LegoPackets.LOGIN_SUCCESS
    elif(q == None):
        conn.commit()
        conn.close()
        return LegoPackets.LOGIN_WRONG_INFO
    else:
        conn.commit()
        conn.close()
        return LegoPackets.LOGIN_BANNED

def getAccountByUsername(username):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM Accounts WHERE Username = '"+username+"'")
    q = c.fetchone()
    conn.commit()
    conn.close()
    return q

def getAccountByAccountID(account):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM Accounts WHERE ID = '"+str(account)+"'")
    q = c.fetchone()
    conn.commit()
    conn.close()
    return q

def serverQuery(q):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    returnVal = c.execute(q)
    conn.commit()
    conn.close()
    return returnVal

def DBServerStarup():
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("DELETE FROM CurrentSessions")
    c.execute("DELETE FROM World_Objects WHERE LOT = 1")
    c.execute("DELETE FROM Worlds")
    conn.commit()
    conn.close()
    print("Reset Sessions Table")

#State is either 0 (Still Loading In), 1 (In character selection) or 2 (In game)

def registerSession(address, userkey, accountID, state):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    if(getSessionByAccountID(accountID) == None):
        c.execute("INSERT INTO CurrentSessions (AccountID, IPAddress, UserKey, charID, zoneID, State) VALUES ("+accountID+", '"+address+"', '"+userkey+"', NULL, NULL, "+state+")")
    conn.commit()
    conn.close()
    print("Registered Session")

def getSessionByUserKey(userKey):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM CurrentSessions WHERE UserKey = '"+userKey+"'")
    q = c.fetchone()
    conn.commit()
    conn.close()
    return q

def destroySessionWithUserKey(userKey):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("DELETE FROM CurrentSessions WHERE UserKey = '"+userKey+"'")
    conn.commit()
    conn.close()
    print("Destroyed Session")

def destroySessionWithAddress(address):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("DELETE FROM CurrentSessions WHERE IPAddress = '"+address+"'")
    conn.commit()
    conn.close()
    print("Destroyed Session")

def registerOrJoinWorld(zoneID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM Worlds WHERE Zone = '" + zoneID + "'")
    if(c.fetchone() == None):
        c.execute("INSERT INTO Worlds (Zone, OwnerID, Name) VALUES ("+zoneID+", NULL, NULL)")
    conn.commit()
    conn.close()

def updateCharacterZone(zoneID, characterID, accountID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("UPDATE CurrentSessions SET charID = "+str(characterID)+", zoneID = "+str(zoneID)+" WHERE AccountID = " + str(accountID))
    c.execute("UPDATE Characters SET LastZone = " + str(zoneID) + " WHERE AccountID = " + str(accountID) + " AND ObjectID = " + str(characterID))
    conn.commit()
    conn.close()

def setCharacterPos(charID, x, y, z):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("UPDATE Characters SET XPos = "+str(x)+", YPos = "+str(y)+", ZPos = "+str(z)+" WHERE ObjectID = "+str(charID))
    conn.commit()
    conn.close()

def getEquippedItems(charID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT Object FROM Inventory WHERE Owner = "+charID+" AND Equipped = 1")
    equipped = c.fetchall()
    conn.commit()
    conn.close()
    return equipped

def getCharacterItems(charID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT Object FROM Inventory WHERE Owner = "+charID)
    items = c.fetchall()
    conn.commit()
    conn.close()
    return items

def getCompletedMissions(charID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT MissionID FROM CompletedMissions WHERE CharID = " + charID)
    missions = c.fetchall()
    conn.commit()
    conn.close()
    return missions

def getItemInfo(objID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT Quantity, Slot FROM Inventory WHERE Object = " + objID)
    info = c.fetchone()
    conn.commit()
    conn.close()
    return info

def getInventoryInfo(charID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT Object, Quantity, Slot, Linked, SpawnerID FROM Inventory WHERE Owner = " + charID)
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
    conn.commit()
    conn.close()
    return LOT, OBJECT, QUANTITY, LINKED, SPAWNERID, SLOT

def getLOTFromObject(objectID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    print("SELECT LOT FROM Objects WHERE ObjectID = "+objectID)
    c.execute("SELECT LOT FROM Objects WHERE ObjectID = "+objectID)
    item = c.fetchone()
    conn.commit()
    conn.close()
    return item

def getSessionByAccountID(accountID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM CurrentSessions WHERE AccountID = '"+accountID+"'")
    q = c.fetchone()
    conn.commit()
    conn.close()
    return q

def deleteCharacter(objID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("DELETE FROM Characters WHERE ObjectID = "+objID)
    c.execute("DELETE FROM Inventory WHERE Owner = " + objID)
    conn.commit()
    conn.close()
    print("Deleted Character")

def getCharacterDataByID(charID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM Characters WHERE ObjectID = '"+charID+"'")
    q = c.fetchone()
    conn.commit()
    conn.close()
    return q


def getCharacterData(accountID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM Characters WHERE AccountID = '"+accountID+"'")
    q = c.fetchall()
    conn.commit()
    conn.close()
    return len(q), q

def findOpenInventorySlot(charID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT BackpackSpace FROM Characters WHERE ObjectID = "+charID)
    backpack = c.fetchone()
    openSlots = []
    for i in range(backpack[0]):
        openSlots.append(i)
    c.execute("SELECT Slot FROM Inventory WHERE Owner = "+charID)
    takenSlots = c.fetchall()
    for row in takenSlots:
        openSlots.remove(row)
    conn.commit()
    conn.close()
    if(openSlots == []):
        return None
    return openSlots[0]

def addItemsToInventory(charID, LOT, Quantity, slot=None, Linked=0, Equipped=0):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    itemSlot = 0
    if(slot != None):
        itemSlot = slot
    else:
        itemSlot = findOpenInventorySlot(charID)
        if(itemSlot == None):
            conn.commit()
            conn.close()
            return "Inventory Full"
    c.execute("INSERT INTO Inventory (Owner, Object, Quantity, Slot, Linked, Equipped) VALUES ("+str(charID)+", "+str(LOT)+", "+str(Quantity)+", "+str(itemSlot)+", "+str(Linked)+", "+str(Equipped)+")")
    conn.commit()
    conn.close()

def createObject(LOT):
    conn = sqlite3.connect("server.sqlite")
    objID = str(randint(1000000000, 9999999999))
    c = conn.cursor()
    c.execute("INSERT INTO Objects (ObjectID, LOT, SpawnID) VALUES ("+objID+", "+str(LOT)+", NULL)")
    conn.commit()
    conn.close()
    return objID

def createMinifigure(AccountID, Name, ShirtColor, ShirtStyle, PantsColor, HairStyle, HairColor, lh, rh, Eyebrows, Eyes, Mouth):
    conn = sqlite3.connect("server.sqlite")
    objID = str(randint(1000000000,9999999999))
    username = Name
    if(Name == ""):
        username = objID
    c = conn.cursor()
    c.execute("INSERT INTO Characters (AccountID, Name, ObjectID, ShirtColor, ShirtStyle, PantsColor, HairStyle, HairColor, lh, rh, Eyebrows, Eyes, Mouth, LastZone, MapInstance, MapClone, Level, Currency, isAlive, UScore, BackpackSpace) VALUES ("+AccountID+", '"+username+"', "+objID+", "+ShirtColor+", "+ShirtStyle+", "+PantsColor+", "+HairStyle+", "+HairColor+", "+lh+", "+rh+", "+Eyebrows+", "+Eyes+", "+Mouth+", 0, 0, 0, 1, 0, 1, 0, 20)")
    conn.commit()
    conn.close()
    pantsObj = createObject(getPantsID(int(PantsColor)))
    shirtObj = createObject(getShirtID(int(ShirtColor), int(ShirtStyle)))
    addItemsToInventory(objID, pantsObj, 1, slot=2, Linked=1, Equipped=1)
    addItemsToInventory(objID, shirtObj, 1, slot=1, Linked=1, Equipped=1)
    print("Created Minifigure " + username)

def getSessionBySessionID(sessionID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM CurrentSessions WHERE SessionID = '"+sessionID+"'")
    q = c.fetchone()
    conn.commit()
    conn.close()
    return q

def getSessionByAddress(address):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("SELECT * FROM CurrentSessions WHERE IPAddress = '"+address+"'")
    q = c.fetchone()
    conn.commit()
    conn.close()
    return q

def updateSessionByUserKey(userkey, state, zoneID, charID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("UPDATE CurrentSessions SET charID = "+charID+", zoneID = "+zoneID+", State = "+state+" WHERE UserKey = '"+userkey+"'")
    conn.commit()
    conn.close()

def updateSessionByAccountID(accountID, state, zoneID, charID):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("UPDATE CurrentSessions SET charID = "+str(charID)+", zoneID = "+str(zoneID)+", State = "+str(state)+" WHERE AccountID = "+str(accountID))
    conn.commit()
    conn.close()

def registerWorldObject(Name, LOT, ObjectID, Zone, posX, posY, posZ, rotX, rotY, rotZ, rotW):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute(
        "INSERT INTO World_Objects (Name, LOT, ObjectID, Zone, posX, posY, posZ, rotX, rotY, rotZ, rotw) VALUES ('"+str(Name)+"', "+str(LOT)+", "+str(ObjectID)+", "+str(Zone)+", "+str(posX)+", "+str(posY)+", "+str(posZ)+", "+str(rotX)+", "+str(rotY)+", "+str(rotZ)+", "+str(rotW)+")")
    conn.commit()
    conn.close()

def updateWorldObject(ObjectID, posX, posY, posZ, rotX, rotY, rotZ, rotW):
    conn = sqlite3.connect("server.sqlite")
    c = conn.cursor()
    c.execute("UPDATE World_Objects SET posX = " + str(posX) + ", posY = " + str(posY) + ", posZ = " + str(posZ) + ", rotX = " + str(rotX) + ", rotY = " + str(rotY) + ", rotZ = " + str(rotZ) + ", rotW = " + str(rotW) +  " WHERE ObjectID = " + str(ObjectID))
    conn.commit()
    conn.close()
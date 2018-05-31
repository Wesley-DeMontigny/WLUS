from passlib.hash import sha256_crypt
from GameManager import Character
from ServerUtilities import getPantsID, getShirtID
import random

class AccountManager():
	def __init__(self):
		self.Accounts = []

	def registerAccount(self, Username: str, Password: str):
		account = Account(self)
		account.Username = Username
		account.Password = sha256_crypt.encrypt(Password)
		account.AccountID = len(self.Accounts) + 1
		account.Banned = False
		self.Accounts.append(account)

	def getAccountByUsername(self, Username: str):
		for Account in self.Accounts:
			if (Account.Username == Username):
				return Account
		return None

	def getCharacterByObjectID(self, ObjectID : int):
		for Account in self.Accounts:
			for Character in Account.Characters:
				if(Character.ObjectConfig["ObjectID"] == ObjectID):
					return Character
		return None


class Account():
	def __init__(self, Parent):
		self.Parent = Parent
		self.Username: str = None
		self.Password: str = None
		self.Banned: bool = False
		self.Characters: list = []
		self.AccountID : int = 0

	def CreateMinifigure(self, Name: str, ShirtColor: int, ShirtStyle: int, PantsColor: int, HairColor: int,
						 HairStyle: int, lh: int, rh: int, Eyebrows: int, Eyes: int, Mouth: int):
		Minifigure = Character(self)
		Minifigure.Zone = 1000
		Minifigure.ObjectConfig["Name"] = Name
		Minifigure.ObjectConfig["ShirtColor"] = ShirtColor
		Minifigure.ObjectConfig["ShirtStyle"] = ShirtStyle
		Minifigure.ObjectConfig["PantsColor"] = PantsColor
		Minifigure.ObjectConfig["HairColor"] = HairColor
		Minifigure.ObjectConfig["HairStyle"] = HairStyle
		Minifigure.ObjectConfig["lh"] = lh
		Minifigure.ObjectConfig["rh"] = rh
		Minifigure.ObjectConfig["ObjectID"] = random.randint(100000000000000000, 999999999999999999)
		Minifigure.ObjectConfig["Eyebrows"] = Eyebrows
		Minifigure.ObjectConfig["Eyes"] = Eyes
		Minifigure.ObjectConfig["Mouth"] = Mouth
		shirtLOT = getShirtID(ShirtColor, ShirtStyle)
		pantsLOT = getPantsID(PantsColor)
		Minifigure.ObjectConfig["Inventory"].addItem(shirtLOT, Equipped=True)
		Minifigure.ObjectConfig["Inventory"].addItem(pantsLOT, Equipped=True)
		self.Characters.append(Minifigure)
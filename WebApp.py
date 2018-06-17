from flask import Flask, request, render_template
from passlib.hash import sha256_crypt
from Enum import *
import time
from io import StringIO
import sys

class ServerApp():
	def __init__(self, ServerName : str, ServerVesion : str, Port : int, AdminUsername : str, AdminPassword : str, WorldServer, AuthServer, AccountManager):
		self.app = Flask("WLUS Web App")
		self.ServerName = ServerName
		self.World = WorldServer
		self.Auth = AuthServer
		self.Port = Port
		self.AccountManager = AccountManager
		self.ServerVersion = ServerVesion
		self.AdminPassword = AdminPassword
		self.AdminUsername = AdminUsername
		self.Sessions = {}

		@self.app.route("/")
		def index():
			if(request.remote_addr not in self.Sessions):
				return render_template("login.html", ServerName = self.ServerName, ServerVersion=self.ServerVersion)
			else:
				MyCharacters = []
				MyAccount = self.World.Game.getAccountByUsername(self.Sessions[request.remote_addr]["User"])
				if(MyAccount is not None):
					for character in MyAccount.Characters:
						MyCharacters.append({"Name":character.ObjectConfig["Name"], "Zone":character.Zone})
				SessionList = []
				for session in self.World.Game.Sessions:
					SessionList.append({"Zone":session.ZoneID, "ObjectID":session.ObjectID, "UserKey":session.userKey, "Name":session.accountUsername, "Addr":str(session.address)})
				ZoneList = []
				for zone in self.World.Game.Zones:
					ZoneList.append({"Zone":zone.ZoneID, "SpawnLoc":str(zone.SpawnLocation.X) + ", " + str(zone.SpawnLocation.Y) + ", " + str(zone.SpawnLocation.Z), "Activity":str(zone.ActivityWorld), "Name":zone.ZoneName})
				AccountList = []
				for account in self.AccountManager.Accounts:
					AccountList.append({"ID":account.AccountID, "Username":account.Username, "IsAdmin":account.IsAdmin, "Banned":account.Banned})
				return render_template("index.html", ServerName=self.ServerName, ServerVersion=self.ServerVersion, User=self.Sessions[request.remote_addr]["User"], Admin=self.Sessions[request.remote_addr]["Admin"],
									   MyCharacters=MyCharacters, Sessions=SessionList, Zones=ZoneList, Accounts=AccountList)

		@self.app.route("/handleLogin", methods=["POST"])
		def handleLogin():
			content = request.get_json()
			username = content.get('username')
			password = content.get('password')
			loginType = content.get('loginType')
			if(loginType == "Admin"):
				result = self.AdminLogin(username, password)
				if(result == LoginResponseEnum.Success):
					self.Sessions[request.remote_addr] = {"User":username,"Admin":True}
					time.sleep(.1)
					return "True"
				else:
					return "False"
			else:
				result = self.BasicLogin(username, password)
				if(result == LoginResponseEnum.Success):
					self.Sessions[request.remote_addr] = {"User":username,"Admin":False}
					time.sleep(.1)
					return "True"
				else:
					return "False"

		@self.app.route("/registerAccount", methods=["POST"])
		def handleRegistration():
			content = request.get_json()
			username = content.get('username')
			password = content.get('password')
			return str(self.RegisterAccount(username, password))

		@self.app.route("/Objects/<zoneID>")
		def getObjects(zoneID):
			if(request.remote_addr in self.Sessions):
				World = self.World.Game.getZoneByID(int(zoneID))
				if(self.Sessions[request.remote_addr]["Admin"] == True):
					if(World is not None):
						ObjectList = []
						for object in World.Objects:
							ObjectList.append({"ObjectID":object.ObjectConfig["ObjectID"], "SpawnerID":object.ObjectConfig["SpawnerID"], "LOT":object.ObjectConfig["LOT"],
											   "Position": "{},{},{}".format(object.ObjectConfig["Position"].X,object.ObjectConfig["Position"].Y,object.ObjectConfig["Position"].Z),
											   "ObjectName":object.ObjectConfig["ObjectName"]})
						return render_template("ZoneObjects.html", ServerName=self.ServerName, ServerVersion=self.ServerVersion, Objects=ObjectList)
					else:
						return "Zone not found!"
				else:
					return "Permissions not high enough!"
			else:
				return ""

		@self.app.route("/execute", methods=["POST"])
		def handleCodeExecuteion():
			if(request.remote_addr in self.Sessions):
				if(self.Sessions[request.remote_addr]["Admin"] == True):
					content = request.get_json()
					pyCode = content.get('pyCode')
					old_stdout = sys.stdout
					result = StringIO()
					sys.stdout = result
					eval(pyCode)
					sys.stdout = old_stdout
					return ">>" + pyCode + "<br/>" + str(result.getvalue())
				else:
					return "Permissions not high enough!"
			else:
				return ""


	def RegisterAccount(self, Username : str, Password : str):
		return self.AccountManager.registerAccount(Username, Password, self.Auth.ServerDB)

	def BasicLogin(self, Username : str, Password : str):
		return self.Auth.checkLogin(Username, Password)

	def AdminLogin(self, Username : str, Password : str):
		if (sha256_crypt.verify(Password, self.AdminPassword) and Username == self.AdminUsername):
			return LoginResponseEnum.Success
		else:
			return LoginResponseEnum.InvalidLoginInfo

	def run(self):
		self.app.run(host="0.0.0.0", port=self.Port, debug=False, use_reloader=False)
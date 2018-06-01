import sqlite3
import re

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
		adjFields = str(fieldResult).split("(")
		Fields = re.findall(r'`(.*?)`', adjFields[1])
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
				queryString += "'"+str(Values[keys[x]])+"'" + ","
			else:
				queryString += "'"+str(Values[keys[x]])+"'" + ")"
		c = self.Connection.cursor()
		c.execute(queryString)
		self.Connection.commit()
	def Query(self, QueryStr : str):
		c = self.Connection.cursor()
		c.execute(QueryStr)
	def update(self, Values : dict, Condition : str):
		queryString = "UPDATE " + self.Name + " SET "
		keys = list(Values.keys())
		for i in range(len(keys)):
			if(i != (len(keys) -1)):
				queryString += keys[i] + " = " + "'"+str(Values[keys[i]])+"'" + ", "
			else:
				queryString += keys[i] + " = " + "'"+str(Values[keys[i]])+"'"
		queryString += " WHERE " + Condition
		c = self.Connection.cursor()
		c.execute(queryString)
		self.Connection.commit()
	def delete(self, Condition : str):
		queryString = "DELETE FROM " + self.Name + " WHERE " + Condition
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
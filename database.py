import sqlite3
import re

class DBTable():
	def __init__(self, Name : str, Connection : sqlite3.Connection):
		self._name : str = Name
		self._connection : sqlite3.Connection = Connection
	def select(self, fields : list, condition : str):
		query_string = "SELECT"
		for i in range(len(fields)):
			if(i != (len(fields) -1)):
				query_string += " " + fields[i] + ","
			else:
				query_string += " " + fields[i]
		query_string += " FROM " + self._name
		if(condition != None):
			query_string += " WHERE " + condition
		c = self._connection.cursor()
		query = c.execute(query_string)
		result = query.fetchall()
		rows = []
		for i in range(len(result)):
			dictionary = {}
			for x in range(len(result[i])):
				dictionary[fields[x]] = result[i][x]
			rows.append(dictionary)
		return rows
	def select_all(self, condition : str):
		query_string = "SELECT * FROM " + self._name
		if(condition != None):
			query_string += " WHERE " + condition
		c = self._connection.cursor()
		query = c.execute(query_string)
		result = query.fetchall()
		rows = []
		field_query = c.execute("SELECT sql FROM sqlite_master WHERE name = '{}'".format(self._name))
		field_result = field_query.fetchone()[0]
		adj_fields = str(field_result).split("(")
		fields = re.findall(r'`(.*?)`', adj_fields[1])
		for i in range(len(result)):
			dictionary = {}
			for x in range(len(result[i])):
				dictionary[fields[x]] = result[i][x]
			rows.append(dictionary)
		return rows
	def insert(self, values : dict):
		query_string = "INSERT INTO " + self._name + " ("
		keys = list(values.keys())
		for i in range(len(keys)):
			if(i != (len(keys) -1)):
				query_string += keys[i] + ","
			else:
				query_string += keys[i] + ")"
		query_string += " VALUES ("
		for x in range(len(keys)):
			if (x != (len(keys) - 1)):
				query_string += "'"+str(values[keys[x]])+"'" + ","
			else:
				query_string += "'"+str(values[keys[x]])+"'" + ")"
		c = self._connection.cursor()
		c.execute(query_string)
		self._connection.commit()
	def query(self, query_str : str):
		c = self._connection.cursor()
		c.execute(query_str)
	def update(self, values : dict, condition : str):
		query_string = "UPDATE " + self._name + " SET "
		keys = list(values.keys())
		for i in range(len(keys)):
			if(i != (len(keys) -1)):
				query_string += keys[i] + " = " + "'"+str(values[keys[i]])+"'" + ", "
			else:
				query_string += keys[i] + " = " + "'"+str(values[keys[i]])+"'"
		query_string += " WHERE " + condition
		c = self._connection.cursor()
		c.execute(query_string)
		self._connection.commit()
	def delete(self, condition : str):
		query_string = "DELETE FROM " + self._name + " WHERE " + condition
		c = self._connection.cursor()
		c.execute(query_string)
		self._connection.commit()

class GameDB():
	def __init__(self, database_path : str):
		self._connection = sqlite3.connect(database_path, check_same_thread=False)
		c = self._connection.cursor()
		table_list = c.execute("SELECT name FROM sqlite_master")
		self.tables : dict = {}
		for table in table_list:
			self.tables[table[0]] = DBTable(table[0], self._connection)
import game_types
import threading

class Script():
	def __init__(self, parent, script_name :str = "", script_path : str = ""):
		self._parent = parent
		self._name : str = script_name
		self._script_path : str = script_path

	def set_path(self, script_path : str):
		self._script_path = script_path

	def set_name(self, name):
		self._name = name

	def get_name(self):
		return self._name

	def get_parent(self):
		return self._parent

	def run(self):
		script_file = open(self._script_path, 'r')
		script_str = script_file.read()
		exec(script_str)


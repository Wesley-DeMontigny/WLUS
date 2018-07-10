import game_types
import threading

'''
Scripts can be attached to just about any object.
'''

class Script():
	def __init__(self, parent, script_name :str = ""):
		self._parent = parent
		self._name : str = script_name

	def get_name(self):
		return self._name

	def get_parent(self):
		return self._parent

	def run(self):
		pass


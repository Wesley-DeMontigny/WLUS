import typing
import game_types
import ctypes
import threading
import random

'''
The Game class is the parent of all other objects in the game.
Things should ALWAYS be implmented through either a service or a script
'''


class Game(game_types.BaseObject):
	def __init__(self):
		super().__init__(None)
		self._name = "Game"
		self._services = []
		self._config : dict = {}
		self._event_handlers = {}

	def start(self):
		for service in self._services:
			service_thread = game_types.GameThread(target=service.initialize)
			service_thread.start()
		self.trigger_event("GameStarted")

	def generate_object_id(self):
		id = random.randint(100000000000000000, 999999999999999999)
		return id

	def register_service(self, service):
		self._services.append(service)
		self.trigger_event("ServiceRegistered", args=(service,), debug=False)

	def register_event_handler(self, event_id : str):
		def register_handler(handler):
			self._event_handlers[handler] = event_id
		return register_handler

	def trigger_event(self, event_id, args : typing.Tuple =(), debug : bool = False):
		handler_activated = False
		for handler in self._event_handlers:
			if(self._event_handlers[handler] == event_id):
				handler_thread = threading.Thread(target=handler, args=args)
				handler_thread.start()
				handler_activated = True
		if(handler_activated != True and debug):
			print("{} Had No Handler!".format(event_id))


	def get_service(self, service_name : str):
		for service in self._services:
			if(service.get_name() == service_name):
				return service
		return None

	def set_config(self, key : str, value : typing.Any):
		self._config[key] = value

	def remove_config(self, key : str):
		del self._config[key]

	def get_pyobject(self, id):
		return ctypes.cast(id, ctypes.py_object).value

	def get_config(self, key : str):
		if(key in self._config):
			return self._config[key]
		else:
			return None

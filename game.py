import typing
import game_types
import ctypes

class Game(game_types.BaseObject):
	def __init__(self):
		super().__init__(None)
		self._name = "Game"
		self._services = []
		self._config : dict = {}

	def start(self):
		for service in self._services:
			service_thread = game_types.GameThread(target=service.initialize)
			service_thread.start()

	def register_service(self, service):
		self._services.append(service)

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

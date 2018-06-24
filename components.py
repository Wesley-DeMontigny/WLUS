import game_types
import typing

'''
Components are used to attach specific values to game objects
'''

class Component():
	def __init__(self, parent):
		self._parent = parent
		self._name = "Base Component"

	def get_name(self):
		return self._name

	def get_parent(self):
		return self._parent


class Transform(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Transform"
		self.position = ComponentProperty(self, game_types.Vector3(), read_only=False)
		self.rotation = ComponentProperty(self, game_types.Vector4(), read_only=False)
		self.scale = ComponentProperty(self, 1, read_only=False)


class ComponentProperty():
	def __init__(self, component : Component, value : typing.Any, read_only : bool = False, expected_type = typing.Any):
		self._component : Component = component
		self._value = value
		self._read_only = read_only
		self._expected_type = expected_type

	def __get__(self, instance, owner):
		return self._value

	def __set__(self, instance, value):
		if(self._read_only == False):
			if(self._expected_type == typing.Any or isinstance(value, self._expected_type)):
				self._component.get_parent().update()
				self._value = value
			else:
				raise Exception("{} expected type {}".format(self, self._expected_type))
		else:
			raise Exception("{} is read only".format(self))

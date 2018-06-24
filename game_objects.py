import game_types
import components
from pyraknet.bitstream import *

'''
GameObjects are objects placed inside scenes
'''

class GameObject(game_types.BaseObject):
	def __init__(self, parent, scene, name : str = "GameObject"):
		super().__init__(parent)
		self._name = name
		self._components = []
		self._scene = scene

	def add_component(self, component):
		self._components.append(component)

	def get_component(self, component):
		for object_component in self._components:
			if(object_component.__class__ == component.__class__):
				return object_component

	def update(self):
		self._scene.update(self)

class ReplicaObject(GameObject):
	def __init__(self, parent, scene, name : str = "GameObject"):
		super().__init__(parent, scene, name)

	def serialize(self):
		pass

	def construct(self):
		pass

import game_types
import components
from pyraknet.bitstream import *

'''
GameObjects are objects placed inside scenes
'''

class GameObject(game_types.BaseObject):
	def __init__(self, parent, scene, object_id : int = None, name : str = "GameObject"):
		super().__init__(parent)
		self._name = name
		self._components = []
		self._scene = scene
		global game
		game = scene.get_parent().get_parent().get_parent()
		if(object_id is None):
			self._object_id = game.generate_object_id()
		else:
			self._object_id = object_id

	def add_component(self, component):
		self._components.append(component)

	def get_component(self, component):
		for object_component in self._components:
			if(object_component.__class__ == component.__class__):
				return object_component

	def get_object_id(self):
		return self._object_id

	def update(self):
		self._scene.update(self)

class ReplicaObject(GameObject):
	def __init__(self, parent, scene, object_id : int = None, name : str = "GameObject"):
		super().__init__(parent, scene, object_id, name)
		self.add_component(components.Transform)

	def serialize(self):
		pass

	def construct(self):
		pass

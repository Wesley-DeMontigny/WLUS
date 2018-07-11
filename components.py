import game_types
import typing
import copy

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

	def __setattr__(self, key, value):
		super().__setattr__(key, value)
		self.get_parent().update()


class Transform(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Transform"
		self.scale : int = 1
		self.position : game_types.Vector3 = game_types.Vector3()
		self.rotation : game_types.Vector4 = game_types.Vector4()
		self.velocity : game_types.Vector3 = game_types.Vector3()
		self.on_ground : bool = True
		self.angular_velocity : game_types.Vector3 = game_types.Vector3()

class Collectible(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Collectible"
		self.collectible_id : int = 0

class Bouncer(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Bouncer"
		self.pet_required : bool = False

#TODO: Implement This Component, It Doesn't Do Anything Now
class Component107(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Component107"

class Character(Component):
	def __init__(self, parent, player_id : int = 0):
		super().__init__(parent)
		self._name = "Character"
		self.player_id : int = player_id
		self.vehicle_id : int = 0
		self.head_glow : int = 0
		self.gm_level : int = 0

	def get_player_info(self):
		game = self.get_parent().zone.get_parent().get_parent()
		player = game.get_service("Player").get_player_by_id(self.player_id)
		account = game.get_service("Player").get_account_by_player_id(self.player_id)
		return copy.deepcopy(player), copy.deepcopy(account)

class Minifig(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Minfig"
		self.head : int = 0
		self.chest : int = 0
		self.legs : int = 0
		self.hair_style : int = 0
		self.hair_color : int = 0
		self.chest_decal : int = 0
		self.head_color : int = 0
		self.left_hand : int = 0
		self.right_hand : int = 0
		self.eyebrows : int = 0
		self.eyes : int = 0
		self.mouth : int = 0

class Possessable(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Possessable"
		self.driver_object_id : int = 0

#TODO: Implement This Component, It Doesn't Do Anything Now
class Vendor(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Vendor"


class PhysicsEffect(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "PhysicsEffect"
		self.effect_type : int = 0
		self.effect_amount : float = 0.0
		self.effect_direction : game_types.Vector3 = game_types.Vector3()

class VehiclePhysics(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "VehiclePhysics"
		self.data_1 : int = 0
		self.flag_1 : bool = False
		self.flag_2 : bool = False
		self.flag_2_1 : bool = False


#TODO: Implement This Component, It Doesn't Do Anything Now
class RacingControl(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "RacingControl"


# TODO: Implement This Component, It Doesn't Do Anything Now
class ScriptedActivity(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "ScriptedActivity"

#TODO: Implement This Component, It Doesn't Do Anything Now
class Skill(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Skill"

class Switch(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Switch"
		self.state : bool = False

class Trigger(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self.tigger_id : int = 0

class ModelData(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "ModelData"
		self.ldf : game_types.LDF = game_types.LDF()

class Render(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Render"
		self.render_disabled : bool = False
		self.fx_effects : list = []

	def add_fx_effect(self, name, effect_id, effect_type, scale, secondary):
		self.fx_effects.append(({"name":name, "effect_id":effect_id, "effect_type":effect_type, "scale":scale, "secondary":secondary}))

#TODO: Implement This Component, It Doesn't Do Anything Now
class ModuleAssembly(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "ModuleAssembly"

class LUPExhibit(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "LUPExhibit"
		self.exhibited_lot : int = 10781

#TODO: Implement This Component, It Doesn't Do Anything Now
class ScriptComponent(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "ScriptComponent"

class Pet(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Pet"
		self.owner_id : int= 0
		self.pet_name : str = "Petty The Pet"

class Stats(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Stats"
		self.health : int = 0
		self.max_health : int = 0
		self.armor : int = 0
		self.max_armor : int = 0
		self.imagination : int = 0
		self.max_imagination : int = 0
		self.faction : int = 0
		self.is_smashable : bool = False
		self.level : int = 1

#TODO: Implement This Component, It Doesn't Do Anything Now
class Destructible(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Destructible"

class Inventory(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Inventory"
		self.items : list = []

	def add_item(self, item):
		self.items.append(item)

class BaseCombatAI(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "BaseCombatAI"
		self.action : int = 0
		self.target_id : int = 0

class Rebuild(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Rebuild"
		self.rebuild_state : int = 0
		self.success : bool = False
		self.enabled : bool = True
		self.time_since_start :float = 0.0
		self.reset_time : float = 0.0
		self.build_activator_pos : game_types.Vector3 = game_types.Vector3()

#TODO: Implement this component
class MovingPlatform(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "MovingPLatform"

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


class Transform(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Transform"
		self.position = ComponentProperty(self, game_types.Vector3(), read_only=False,  expected_type=game_types.Vector3)
		self.rotation = ComponentProperty(self, game_types.Vector4(), read_only=False, expected_type=game_types.Vector4)
		self.velocity = ComponentProperty(self, game_types.Vector3(), read_only=False, expected_type=game_types.Vector3)
		self.on_ground = ComponentProperty(self, True, read_only=False, expected_type=bool)
		self.angular_velocity = ComponentProperty(self, game_types.Vector3(), read_only=False, expected_type=game_types.Vector3)
		self.scale = ComponentProperty(self, 1, read_only=False, expected_type=int)

class Collectible(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Collectible"
		self.collectible_id = ComponentProperty(self, 0, read_only=False, expected_type=int)

class Bouncer(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Bouncer"
		self.pet_required = ComponentProperty(self, False, read_only=False, expected_type=bool)

class Component107(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Component107"
		self.flag_1 = ComponentProperty(self, False, read_only=False, expected_type=bool)
		self.data_1_1 = ComponentProperty(self, 0, read_only=False, expected_type=int)

class Character(Component):
	def __init__(self, parent, player_id : int = 0):
		super().__init__(parent)
		self._name = "Character"
		self.player_id = ComponentProperty(self, player_id, read_only=False, expected_type=int)
		self.pvp_enabled = ComponentProperty(self, False, read_only=False, expected_type=bool)
		self.vehicle_id = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.head_glow = ComponentProperty(self, 0, read_only=False, expected_type=bool)
		self.gm_level = ComponentProperty(self, 0, read_only=False, expected_type=int)

	def get_player_info(self):
		game = self.get_parent().scene.get_parent().get_parent()
		player = game.get_service("Player").get_player_by_id(self.player_id)
		account = game.get_service("Player").get_account_by_player_id(self.player_id)
		return copy.deepcopy(player), copy.deepcopy(account)

class Minifig(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Minfig"
		self.head = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.chest = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.legs = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.hair_style = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.hair_color = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.chest_decal = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.head_color = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.left_hand = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.right_hand = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.eyebrows = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.eyes = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.mouth = ComponentProperty(self, 0, read_only=False, expected_type=int)

class Possessable(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Possessable"
		self.driver_object_id = ComponentProperty(self, 0, read_only=False, expected_type=int)

class Vendor(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Vendor"
		self.flag_1 = ComponentProperty(self, False, read_only=False, expected_type=bool)
		self.flag_1_1 = ComponentProperty(self, False, read_only=False, expected_type=bool)
		self.flag_1_2 = ComponentProperty(self, False, read_only=False, expected_type=bool)

class PhysicsEffect(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "PhysicsEffect"
		self.effect_type = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.effect_amount = ComponentProperty(self, 0.0, read_only=False, expected_type=float)
		self.effect_direction = ComponentProperty(self, game_types.Vector3(), read_only=False, expected_type=game_types.Vector3)

class VehiclePhysics(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "VehiclePhysics"
		self.data_1 = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.flag_1 = ComponentProperty(self, False, read_only=False, expected_type=bool)
		self.flag_2 = ComponentProperty(self, False, read_only=False, expected_type=bool)
		self.flag_2_1 = ComponentProperty(self, False, read_only=False, expected_type=bool)

#TODO: Implement this
class RacingControl(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "RacingControl"
		self.flag_1 = ComponentProperty(self, False, read_only=True, expected_type=bool)
		self.flag_2 = ComponentProperty(self, False, read_only=True, expected_type=bool)
		self.flag_3 = ComponentProperty(self, False, read_only=True, expected_type=bool)
		self.flag_4 = ComponentProperty(self, False, read_only=True, expected_type=bool)
		self.flag_5 = ComponentProperty(self, False, read_only=True, expected_type=bool)


#TODO: Implment this
class ScriptedActivity(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "ScriptedActivity"
		self.flag_1 = ComponentProperty(self, False, read_only=True, expected_type=bool)

class Skill(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Skill"
		self.flag_1 = ComponentProperty(self, False, read_only=False, expected_type=bool)

class Switch(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Switch"
		self.state = ComponentProperty(self, False, read_only=False, expected_type=bool)

class Trigger(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self.tigger_id = ComponentProperty(self, 0, read_only=False, expected_type=int)

class ModelData(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "ModelData"
		self.ldf = game_types.LDF()

class Render(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Render"
		self.render_disabled = ComponentProperty(self, False, read_only=False, expected_type=bool)
		self.fx_effects = ComponentProperty(self, [], read_only=False, expected_type=list)

	def add_fx_effect(self, name, effect_id, effect_type, scale, secondary):
		self.fx_effects = self.fx_effects.append(({"name":name, "effect_id":effect_id, "effect_type":effect_type, "scale":scale, "secondary":secondary}))

#TODO: Implement
class ModuleAssembly(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "ModuleAssembly"
		self.flag_1 = ComponentProperty(self, False, read_only=True, expected_type=bool)

class LUPExhibit(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "LUPExhibit"
		self.exhibited_lot = ComponentProperty(self, 10781, read_only=False, expected_type=int)

class ScriptComponent(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "ScriptComponent"
		self.flag_1 = ComponentProperty(self, False, read_only=True, expected_type=bool)#Just force this as False for now

class Pet(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Pet"
		self.owner_id = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.pet_name = ComponentProperty(self, "Petty The Pet", read_only=False, expected_type=str)

class Stats(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Stats"
		self.health = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.max_health = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.armor = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.max_armor = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.imagination = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.max_imagination = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.faction = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.is_smashable = ComponentProperty(self, False, read_only=False, expected_type=bool)

class Destructible(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Destructible"
		self.flag_1 = ComponentProperty(self, False, read_only=True, expected_type=bool)#Just force these two as False until the structure is researched more
		self.flag_2 = ComponentProperty(self, False, read_only=True, expected_type=bool)

class Inventory(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Inventory"
		self.items = ComponentProperty(self, [], read_only=False, expected_type=list)

class BaseCombatAI(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "BaseCombatAI"
		self.action = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.target_id = ComponentProperty(self, 0, read_only=False, expected_type=int)

class Rebuild(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Rebuild"
		self.rebuild_state = ComponentProperty(self, 0, read_only=False, expected_type=int)
		self.success = ComponentProperty(self, False, read_only=False, expected_type=bool)
		self.enabled = ComponentProperty(self, True, read_only=False, expected_type=bool)
		self.time_since_start = ComponentProperty(self, 0.0, read_only=False, expected_type=float)
		self.reset_time = ComponentProperty(self, 0.0, read_only=False, expected_type=float)
		self.build_activator_pos = ComponentProperty(self, game_types.Vector3(), read_only=False, expected_type=game_types.Vector3)

#TODO: Implement this component
class MovingPlatform(Component):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "MovingPLatform"
		self.flag_1 = ComponentProperty(self, False, read_only=True, expected_type=bool)

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
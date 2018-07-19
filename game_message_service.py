import services
from pyraknet.bitstream import *
import game_enums
import game_types
import copy


class GameMessageService(services.GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Game Message"
		global game
		game = self.get_parent()

	def initialize(self):
		self.world_server = game.get_service("World Server").server
		super().initialize()

	def send_game_msg(self, object_id, msg_id, recipients: list, additional_parameters: list = None):
		msg = WriteStream()
		msg.write(game_enums.PacketHeaderEnum.SERVER_GAME_MESSAGE.value)
		msg.write(c_longlong(object_id))
		msg.write(c_ushort(msg_id))
		self.world_server.send(msg, recipients)

	def play_fx_effect(self, object_id : int, recipients : list, effect_id : int, effect_type : str, scale : float, name : str, priority : float = 1.0, secondary : int = -1, serialize : bool = True):
		msg = WriteStream()
		msg.write(game_enums.PacketHeaderEnum.SERVER_GAME_MESSAGE.value)
		msg.write(c_longlong(object_id))
		msg.write(c_ushort(game_enums.GameMessages.PLAY_FX_EFFECT.value))

		msg.write(c_bit(effect_id != -1))
		if(effect_id != -1):
			msg.write(c_long(effect_id))

		msg.write(effect_type, length_type=c_ulong)

		msg.write(c_bit(scale != 1.0))
		if(scale != 1.0):
			msg.write(c_float(scale))

		msg.write(game_types.String(name, length_type=c_ulong))

		msg.write(c_bit(priority != 1.0))
		if(priority != 1.0):
			msg.write(c_float(priority))

		msg.write(c_bit(secondary > -1))
		if(secondary > -1):
			msg.write(c_longlong(secondary))

		msg.write(c_bit(serialize))

		self.world_server.send(msg, recipients)

	def stop_fx_effect(self, object_id : int, recipients : list, kill_immediately : bool, name : str):
		msg = WriteStream()
		msg.write(game_enums.PacketHeaderEnum.SERVER_GAME_MESSAGE.value)
		msg.write(c_longlong(object_id))
		msg.write(c_ushort(game_enums.GameMessages.PLAY_FX_EFFECT.value))

		msg.write(c_bit(kill_immediately))
		msg.write(game_types.String(name, length_type=c_ulong))
		self.world_server.send(msg, recipients)

	def add_item_to_inventory_client_sync(self, object_id : int, recipients : list, lot : int, item_id : int, slot_id : int, bound: bool = False, bound_on_equip : bool = False, bound_on_pickup : bool = False, loot_type_source : int = 0, extra_info : str = "", sub_key : int = 0, inventory_type : int = 0, item_count : int = 1, items_total : int = 0, flying_loot_pos : game_types.Vector3 = game_types.Vector3(), show_flying_loot : bool = True):
		msg = WriteStream()
		msg.write(game_enums.PacketHeaderEnum.SERVER_GAME_MESSAGE.value)
		msg.write(c_longlong(object_id))
		msg.write(c_ushort(game_enums.GameMessages.ADD_ITEM_TO_INVENTORY_CLIENT_SYNC.value))

		msg.write(c_bit(bound))
		msg.write(c_bit(bound_on_equip))
		msg.write(c_bit(bound_on_pickup))

		msg.write(c_bit(loot_type_source != 0))
		if(loot_type_source != 0):
			msg.write(c_int(loot_type_source))

		msg.write(extra_info, length_type=c_ulong)
		msg.write(c_ulong(lot))

		msg.write(c_bit(sub_key != 0))
		if(sub_key != 0):
			msg.write(c_longlong(sub_key))

		msg.write(c_bit(inventory_type != 0))
		if(inventory_type != 0):
			msg.write(c_int(inventory_type))

		msg.write(c_bit(item_count != 1))
		if(item_count != 1):
			msg.write(c_ulong(item_count))

		msg.write(c_bit(items_total != 0))
		if(items_total != 0):
			msg.write(c_ulong(items_total))

		msg.write(c_longlong(item_id))

		msg.write(c_float(flying_loot_pos.X))
		msg.write(c_float(flying_loot_pos.Y))
		msg.write(c_float(flying_loot_pos.Z))

		msg.write(c_bit(show_flying_loot))

		msg.write(c_int(slot_id))

		self.world_server.send(msg, recipients)

	def remove_skill(self, object_id : int, recipients : list, skill_id : int, from_skill_set : bool = False):
		msg = WriteStream()
		msg.write(game_enums.PacketHeaderEnum.SERVER_GAME_MESSAGE.value)
		msg.write(c_longlong(object_id))
		msg.write(c_ushort(game_enums.GameMessages.REMOVE_SKILL.value))

		msg.write(c_bit(from_skill_set))

		msg.write(c_int(skill_id))

		self.world_server.send(msg, recipients)

	def echo_start_skill(self, object_id : int, recipients : list, skill_id : int, bit_stream:str, optional_originator : int, used_mouse : bool = False, caster_latency : float = 0.0, cast_type : int = 0, last_clicked_pos : game_types.Vector3 = game_types.Vector3(), optional_target_id : int = 0, originator_rot : game_types.Vector4 = game_types.Vector4(), ui_skill_handle : int = 0):
		msg = WriteStream()
		msg.write(game_enums.PacketHeaderEnum.SERVER_GAME_MESSAGE.value)
		msg.write(c_longlong(object_id))
		msg.write(c_ushort(game_enums.GameMessages.ECHO_START_SKILL.value))

		msg.write(c_bit(used_mouse))

		msg.write(c_bit(caster_latency != 0.0))
		if(caster_latency != 0.0):
			msg.write(c_float(caster_latency))

		msg.write(c_bit(cast_type != 0))
		if(cast_type != 0):
			msg.write(c_int(cast_type))

		msg.write(c_bit(last_clicked_pos != game_types.Vector3()))
		if(last_clicked_pos != game_types.Vector3()):
			msg.write(c_float(last_clicked_pos.X))
			msg.write(c_float(last_clicked_pos.Y))
			msg.write(c_float(last_clicked_pos.Z))

		msg.write(c_longlong(optional_originator))

		msg.write(c_bit(optional_target_id != 0))
		if(optional_target_id != 0):
			msg.write(c_longlong(optional_target_id))

		msg.write(c_bit(originator_rot != game_types.Vector4()))
		if(originator_rot != game_types.Vector4()):
			msg.write(c_float(originator_rot.X))
			msg.write(c_float(originator_rot.Y))
			msg.write(c_float(originator_rot.Z))
			msg.write(c_float(originator_rot.W))

		msg.write(bit_stream, length_type=c_ulong)

		msg.write(c_ulong(skill_id))

		msg.write(c_bit(ui_skill_handle != 0))
		if(ui_skill_handle != 0):
			msg.write(c_ulong(0))

		self.world_server.send(msg, recipients)

	def add_skill(self, object_id : int, recipients : list, skill_id : int, ai_combat_weight : int = 0, from_skill_set : bool = False, cast_type : int = 0, time_secs : float = -1.0, times_can_cast : int = -1, slot_id : int = -1, temporary : bool = True):
		msg = WriteStream()
		msg.write(game_enums.PacketHeaderEnum.SERVER_GAME_MESSAGE.value)
		msg.write(c_longlong(object_id))
		msg.write(c_ushort(game_enums.GameMessages.ADD_SKILL.value))

		msg.write(c_bit(ai_combat_weight != 0 and ai_combat_weight is not None))
		if(ai_combat_weight != 0 and ai_combat_weight is not None):
			msg.write(c_int(ai_combat_weight))

		msg.write(c_bit(from_skill_set))

		msg.write(c_bit(cast_type != 0))
		if(cast_type != 0):
			msg.write(c_int(cast_type))

		msg.write(c_bit(time_secs > -1.0))
		if(time_secs > -1.0):
			msg.write(c_float(time_secs))

		msg.write(c_bit(times_can_cast > -1))
		if(times_can_cast > -1):
			msg.write(c_int(times_can_cast))

		msg.write(c_ulong(skill_id))

		msg.write(c_bit(slot_id > -1))
		if(slot_id > -1):
			msg.write(c_int(slot_id))

		msg.write(c_bit(temporary))

		self.world_server.send(msg, recipients)

	def set_jetpack_mode(self, object_id : int, recipients : list, bypass_checks : bool = True, hover : bool = False, use : bool = False, effect_id : int = -1, air_speed : int = 10, max_air_speed : int = 15, vert_vel : int = 1, warning_effect_id : int = -1):
		msg = WriteStream()
		msg.write(game_enums.PacketHeaderEnum.SERVER_GAME_MESSAGE.value)
		msg.write(c_longlong(object_id))
		msg.write(c_ushort(game_enums.GameMessages.SET_JETPACK_MODE.value))

		msg.write(c_bit(bypass_checks))
		msg.write(c_bit(hover))
		msg.write(c_bit(use))

		msg.write(c_bit(effect_id != -1))
		if(effect_id != -1):
			msg.write(c_int(effect_id))

		msg.write(c_bit(air_speed != 10))
		if(air_speed != 10):
			msg.write(c_float(air_speed))

		msg.write(c_bit(max_air_speed != 15))
		if(max_air_speed != 15):
			msg.write(c_float(max_air_speed))

		msg.write(c_bit(vert_vel != 1))
		if(vert_vel != 1):
			msg.write(c_float(vert_vel))

		msg.write(c_bit(warning_effect_id != -1))
		if(warning_effect_id != -1):
			msg.write(c_int(0))

		self.world_server.send(msg, recipients)








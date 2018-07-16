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








import services

class Session():
	def __init__(self):
		self.scene_id = 0
		self.player_id = 0
		self.account_id = 0
		self.address = None
		self.user_key = ""

class SessionService(services.GameService):
	def __init__(self, parent):
		super().__init__(parent)
		self._name = "Session"

		self._sessions = []

	def add_session(self, scene_id = 0, player_id = 0, account_id = 0, address = None, userkey = ""):
		new_session = Session()
		new_session.scene_id = scene_id
		new_session.player_id = player_id
		new_session.account_id = account_id
		new_session.address = address
		new_session.user_key = userkey
		self._sessions.append(new_session)

	def remove_session(self, session : Session):
		self._sessions.remove(session)

	def get_session_by_player_id(self, player_id : int):
		for session in self._sessions:
			if(session.player_id == player_id):
				return session
		return None

	def get_session_by_address(self, address):
		for session in self._sessions:
			if(session.address == address):
				return session
		return None
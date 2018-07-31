import sys
sys.path.append("..")
import scripts

class Main(scripts.Script):
	def __init__(self, parent):
		super().__init__(parent, "Wesley's Zone Editor")
		global game
		game = self.get_parent()

	def run(self):
		game.register_console_command("Register", self.register_handler)

	def register_handler(self, args):
		username = args[0]
		password = args[1]
		auth_service = game.get_service("Auth Server")
		auth_service.register_account(username, password)
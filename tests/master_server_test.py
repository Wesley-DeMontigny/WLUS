import sys
sys.path.append("../")
from core import master_server


server = master_server.MasterServer(('0.0.0.0', 4211))

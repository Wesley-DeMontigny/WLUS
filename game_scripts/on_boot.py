'''
This script will do things that are supposed to happen on bootup
'''


game = self._parent
@game.register_event_handler("ServiceRegistered")
def register_zones(service):
	from game_enums import zone_names
	if(service.get_name() == "World"):
		for zone in zone_names:
			service.register_scene(level=zone, name=zone_names[zone])
			print("Registered {}!".format(zone_names[zone]))
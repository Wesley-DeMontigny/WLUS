


class EventManager:
	def __init__(self):
		#Takes in the following values
		#Name (a string)
		#EventType (a string)
		#HandlingFunction (a function that has 1 argument that is an array)
		self.Events = []
	def registerEvent(self, Name, Type, HandlingFunction):
		self.Events.append({"Name":Name, "EventType":Type, "HandlingFunction":HandlingFunction})
	def runEvent(self, EventType, Arguments):
		for event in self.Events:
			if(EventType == event["EventType"]):
				print(event["Name"] + " was triggered")
				event["HandlingFunction"](Arguments)

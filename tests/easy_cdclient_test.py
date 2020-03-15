import sys
from plugins.easy_cdclient import cdclient_objects

duke = cdclient_objects.GameObject(12261)
print(duke.object_data.__dict__)
for component in duke.components:
    if duke.components[component] is not None:
        if isinstance(duke.components[component], list):
            print(str(component) + " -- ")
            for c in duke.components[component]:
                print(c.__dict__)
        else:
            print(str(component) + " -- " + str(duke.components[component].__dict__))
"""
This contains the PluginManager class.

THIS AINT WORKIN. What should be implemented is a recursive function that goes through each
plugin and makes sure they all have their dependencies. STOP BEING LAZY AND FIX THIS WESLEY

NOTE: Plugin ids should be the same name as their folder.
"""
from typing import List, Dict
import os
import json


class PluginManager:
    """
    Makes sure that all dependencies are needed for the plugins that will be loaded.
    """
    @classmethod
    def get_config(cls, plugin_id: str) -> Dict:
        with open(f"./plugins/{plugin_id}/plugin.json") as json_file:
            config = json.load(json_file)
        return config

    @classmethod
    def get_valid_plugins(cls, plugin_type: str, debug: bool = True) -> List[str]:
        """
        This gets all the plugins which have their dependencies fulfilled.
        :param plugin_type: The type of plugin the function will look for. (ie. an auth server will only want to load auth types)
        :param debug: Determines whether or not the function will output the plugins which aren't valid
        :return: Returns a list of all the plugin directories which should be loaded
        """
        plugins = {}  # Dict of lists of various plugin types
        for folder in next(os.walk('./plugins'))[1]:
            config = PluginManager.get_config(folder)
            if config["type"] in plugins:
                plugins[config["type"]].append((f"./plugins/{folder}/plugin.json", config))
            else:
                plugins[config["type"]] = [(f"./plugins/{folder}/plugin.json", config)]

        valid_plugins = []
        for t in plugin_type.split("-"):
            if t in plugins:
                for plugin, config in plugins[t]:
                    load = [True]
                    for d in config["dependencies"]:
                        has_plugin = False
                        for p_type in plugins:
                            for p in plugins[p_type]:
                                if p[1]["id"] == d:
                                    has_plugin = True
                                    break
                            if has_plugin:
                                break
                        if not has_plugin:
                            load = False
                            if debug:
                                print(f"{config['name']} will not be loaded. Missing dependency: {d}")
                            break
                    if load[0]:
                        valid_plugins.append(config["id"])

        return valid_plugins

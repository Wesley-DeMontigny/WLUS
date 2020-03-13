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
    def _check_dep_recur(cls, plufin_config, plugins):
        """
        This is a recursive function that makes sure every dependency has their own dependencies present
        :param plufin_config: The config of the plugin you are checking
        :param plugins: The list of plugins
        :return: True or False statement
        """
        dep_fullfilled = 0
        for t in plugins:
            for plugin, p_config in plugins[t]:
                if p_config["id"] in plufin_config["dependencies"]:
                    if PluginManager._check_dep_recur(p_config, plugins):
                        dep_fullfilled += 1
                    else:
                        print(f"{plufin_config['name']} will not be loaded. Missing dependency: {p_config['id']}")
        return dep_fullfilled == len(plufin_config["dependencies"])

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
                    if PluginManager._check_dep_recur(config, plugins):
                        valid_plugins.append(config["id"])

        return valid_plugins

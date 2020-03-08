"""
This file contains the game server class.
"""
import pyraknet.server
import pyraknet.messages
import threading
from core.plugin_manager import PluginManager
import importlib
from mysql.connector import connection
import configparser
import socket
import sys


class GameServer(pyraknet.server.Server):
    def __init__(self, address: pyraknet.messages.Address, max_connections: int, incoming_password: bytes,
                 server_type: str, zone: int, name: str):

        super().__init__(address, max_connections, incoming_password)
        self.add_handler(pyraknet.server.Event.UserPacket, self.handle_packet)

        self.name = name
        self.zone = zone
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        self.master_server = socket.socket()
        self.master_server.connect((str(self.config["GENERAL"]["master_server_address"]),
                                    int(self.config["GENERAL"]["master_server_port"])))
        self.master_server.send(str(self.config["GENERAL"]["master_server_password"]).encode("UTF-8"))
        if self.master_server.recv(1024) == b"Accepted":
            print("Successfully Logged Into Master Server")
            self.master_server.send((str(server_type) + "$" + str(address[1]) + "$" + str(zone) + "$" + str(self.name))
                                    .encode("UTF-8"))
            if self.master_server.recv(1024) == b"Registered":
                print("Successfully Registered Server")
            else:
                print("Server Failed Registration")
                sys.exit()
        else:
            print("Server Failed To Login")
            sys.exit()

        self.packet_handlers = {}
        self.db_connection = connection.MySQLConnection(user=self.config["MYSQL"]["user"],
                                                        password=self.config["MYSQL"]["password"],
                                                        host=self.config["MYSQL"]["host"],
                                                        database=self.config["MYSQL"]["database"])

        plugins_to_load = PluginManager.get_valid_plugins(server_type)
        for p in plugins_to_load:
            config = PluginManager.get_config(p)
            plugin_module = importlib.import_module(f"plugins.{p}.{config['main_file']}")
            plugin_module.Plugin(self)

    def redirect_request(self, method: str, identifier: str):
        self.master_server.send(b"r")
        if self.master_server.recv(1024) == b"Redirect Acknowledged":
            self.master_server.send((method + "$" + identifier).encode("UTF-8"))
            data = self.master_server.recv(1024).decode("UTF-8")
            data = data.split("$")
            return str(data[0]), int(data[1])

    def register_handler(self, function, packet_header):
        if packet_header in self.packet_handlers:
            self.packet_handlers[packet_header].append(function)
        else:
            self.packet_handlers[packet_header] = [function]

    def handle_packet(self, data: bytes, address: pyraknet.messages.Address):
        if data[0:8] in self.packet_handlers:
            for f in self.packet_handlers[data[0:8]]:
                handler = threading.Thread(target=f, args=(data[8:], address, self))
                handler.start()

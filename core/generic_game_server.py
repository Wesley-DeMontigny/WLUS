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
import json


class GameServer(pyraknet.server.Server):
    def __init__(self, address: pyraknet.messages.Address, max_connections: int, incoming_password: bytes,
                 server_type: str, zone: int, name: str):

        super().__init__(address, max_connections, incoming_password)
        self.add_handler(pyraknet.server.Event.UserPacket, self.handle_packet)
        self.add_handler(pyraknet.server.Event.Disconnect, self.handle_disconnect)

        self.name = name
        self.zone = zone
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        self.master_server = socket.socket()
        self.master_server.connect((str(self.config["GENERAL"]["master_server_address"]),
                                    int(self.config["GENERAL"]["master_server_port"])))
        self.master_server.send(str(self.config["GENERAL"]["master_server_password"]).encode("UTF-8"))
        if self.master_server.recv(2048) == b"Accepted":
            print("Successfully Logged Into Master Server")
            self.master_server.send((str(server_type) + "$" + str(address[1]) + "$" + str(zone) + "$" + str(self.name))
                                    .encode("UTF-8"))
            if self.master_server.recv(2048) == b"Registered":
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

    def handle_disconnect(self, address: pyraknet.messages.Address):
        print("Disconnected with %s" % str(address))
        session = self.lookup_session_by_ip(address[0])
        if session is not None:
            if session["current_instance"] == self.name:
                self.delete_session(ip_address=address[0])
                print("Deleted session for %s" % str(address))

    def redirect_request(self, method: str, identifier: str):
        self.master_server.send(b"r")
        if self.master_server.recv(2048) == b"Redirect Acknowledged":
            self.master_server.send((method + "$" + identifier).encode("UTF-8"))
            data = self.master_server.recv(2048).decode("UTF-8")
            data = data.split("$")
            return data[0], int(data[1]), data[2]

    def lookup_session_by_ip(self, ip_address: str):
        data = self.execute_master_query("""SELECT * FROM session WHERE ip_address = "%s";""" % ip_address)
        if data:
            return data[0]
        else:
            return None

    def lookup_session_by_username(self, username: str):
        data = self.execute_master_query("""SELECT * FROM session WHERE username = "%s";""" % username)
        if data:
            return data[0]
        else:
            return None

    def update_session_instance(self, instance: str, username: str = None, ip_address: str = None):
        if username is not None:
            self.execute_master_query("""UPDATE session SET current_instance = "%s" WHERE username = "%s";""" %
                                      (instance, username), do_return=False)
        elif ip_address is not None:
            self.execute_master_query("""UPDATE session SET current_instance = "%s" WHERE ip_address = "%s";""" %
                                      (instance, ip_address))

    def delete_session(self, username: str = None, ip_address: str = None):
        if username is not None:
            self.execute_master_query("""DELETE FROM WHERE username = "%s";""" %
                                      username, do_return=False)
        elif ip_address is not None:
            self.execute_master_query("""DELETE FROM session WHERE ip_address = "%s";""" %
                                      ip_address)

    def execute_master_query(self, query: str, do_return=True):
        if do_return:
            msg = ("q^"+query).encode("UTF-8")
            self.master_server.send(msg)
            data = self.master_server.recv(2048).decode("UTF-8")
            return json.loads(data)
        else:
            msg = ("q*"+query).encode("UTF-8")
            self.master_server.send(msg)
            data = self.master_server.recv(2048).decode("UTF-8")
            return data == "Success"

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

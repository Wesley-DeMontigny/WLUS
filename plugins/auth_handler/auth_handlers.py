"""
This plugin will handle all of the auth packet handlers
"""
from ..serializables import packet_enum, auth_to_client, client_to_auth, global_packets
from pyraknet.bitstream import *
import os
import uuid
import bcrypt
from datetime import datetime


class Plugin:
    def __init__(self, parent):
        print("Auth Handler Initiated")
        parent.register_handler(Plugin.handle_handshake, packet_enum.PacketHeader.HANDSHAKE.value)
        parent.register_handler(Plugin.handle_login, packet_enum.PacketHeader.CLIENT_LOGIN_INFO.value)

    @classmethod
    def handle_login(cls, data: bytes, address, server):
        stream = ReadStream(data)
        login_info = stream.read(client_to_auth.LoginInfoPacket)
        print(f"Player logging in with Username [{login_info.username}] and Password [{login_info.password}]")

        packet = WriteStream()
        response = auth_to_client.LoginInfoPacket()

        c = server.db_connection.cursor()
        c.execute("SELECT * FROM account WHERE username = %s", (login_info.username,))
        results = c.fetchone()
        if results is not None:
            user_info = dict(zip(c.column_names, results))
            if (not bool(user_info["banned"]) and
                    bcrypt.checkpw(login_info.password.encode("utf-8"), user_info["password"].encode("utf-8"))
                    and server.lookup_session_by_username(login_info.username) is None):
                response.login_return_code = packet_enum.LoginReturnCode.SUCCESS.value

                response.user_key = (str(uuid.uuid4()))[0:20]
                timestamp = datetime.timestamp(datetime.now())

                server.execute_master_query("""INSERT INTO session(username, user_key, ip_address, login_timestamp, 
                                            current_instance) VALUES ("%s", "%s", "%s", %s, "%s")""" %
                                            (login_info.username, response.user_key, str(address[0]), timestamp,
                                             server.name), do_return=False)

                print(f"Login Succeeded - Created Session with User-key [{response.user_key}] "
                      f"and Timestamp [{timestamp}]")
                c.execute("UPDATE account SET last_login = %s WHERE username = %s", (timestamp, login_info.username))
                server.db_connection.commit()
            elif server.lookup_session_by_username(login_info.username) is not None:
                response.login_return_code = packet_enum.LoginReturnCode.INVALID_LOGIN_INFO
                response.custom_error = "This account already has a session running"
                print("Login Failed")
            else:
                response.login_return_code = packet_enum.LoginReturnCode.INVALID_LOGIN_INFO.value
                print("Login Failed")
        else:
            response.login_return_code = packet_enum.LoginReturnCode.INVALID_LOGIN_INFO.value
            print("Login Failed")

        char_address, char_port, name = server.redirect_request("instance", "char")
        response.char_port = char_port
        response.char_ip = char_address
        server.update_session_instance(name, ip_address=address[0])
        packet.write(packet_enum.PacketHeader.LOGIN_RESPONSE.value)
        packet.write(response)
        server.send(packet, address)

    @classmethod
    def handle_handshake(cls, data: bytes, address, server):
        """
        Handles initial connection between server and client.
        """
        stream = ReadStream(data)
        client_handshake = stream.read(global_packets.HandshakePacket)
        print(f"{address[0]} has initiated handshake - Client has version {client_handshake.game_version}")

        server_handshake = global_packets.HandshakePacket()
        server_handshake.remote_connection_type = 1
        server_handshake.process_id = os.getpid()
        packet = WriteStream()
        packet.write(packet_enum.PacketHeader.HANDSHAKE.value)
        packet.write(server_handshake)
        server.send(packet, address)

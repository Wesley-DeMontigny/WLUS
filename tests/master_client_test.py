import socket
import json


def loop(socket):
    socket.send(("q*" + ("""INSERT INTO session(username, user_key, ip_address, login_timestamp) VALUES
     ("%s", "%s", "%s", %s)""" % ("joe", "aaa", "127.0.0.1", 0))).encode("UTF-8"))
    socket.recv(2048)
    socket.send(b"q^SELECT * FROM session")
    print(json.loads(socket.recv(2048).decode("UTF-8"))[1]["id"])


s = socket.socket()
s.connect(('127.0.0.1', 4211))
s.send(b"1124 WLUS2.0")
if s.recv(2048) == b"Accepted":
    print("Successfully Logged In")
    s.send(b"auth$1001$None$AUTH_1")
    if s.recv(2048) == b"Registered":
        loop(s)

import socket


s = socket.socket()
s.connect(('127.0.0.1', 4211))
s.send(b"1124 WLUS2.0")
if s.recv(1024) == b"Accepted":
    print("Successfully Logged In")
    s.send(b"auth$1001$None$AUTH_1")
    if s.recv(1024) == b"Registered":
        s.send(b"r")
        if s.recv(1024) == b"Redirect Acknowledged":
            s.send(b"instance$auth")
            print(s.recv(1024))


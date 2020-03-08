import socket
import threading


class MasterServer:
    def __init__(self, address: tuple, max_connections: int = 10, password: bytes = b"1124 WLUS2.0"):
        self.address = address
        self.max_connections = max_connections
        self.password = password

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.bind(address)
        self._s.listen(max_connections)
        self._connections = {}

        main_thread = threading.Thread(target=self._run)
        main_thread.start()

    def _run(self):
        print("Starting Master Server")
        while True:
            client_socket, address = self._s.accept()
            password = client_socket.recv(1024)
            print(f"Attempted Login From Address [{address}] With Password [{password.decode('UTF-8')}]")
            if password == self.password:
                client_socket.send(b"Accepted")
                server_info = client_socket.recv(1024)
                data = server_info.decode("UTF-8").split("$")
                if data[2].lower() == 'none':
                    data[2] = None
                print(f"Registered Server With Data: {data}")
                self._connections[data[3]] = {"instance_type": data[0], "port": data[1], "zone": data[2],
                                              "address": address}
                client_socket.send(b"Registered")
                threading.Thread(target=self._client_thread, args=(client_socket, address)).start()
            else:
                client_socket.send(b"Bad Login")
                client_socket.close()

    def _client_thread(self, client_socket: socket, address: tuple):
        while True:
            data = client_socket.recv(1024)
            if len(data.decode("UTF-8")) > 0:
                if data.decode("UTF-8")[0] == "r":
                    client_socket.send(b"Redirect Acknowledged")
                    # Format: <selector_type>$<selector>
                    redirect_data = client_socket.recv(1024).decode("UTF-8").split("$")
                    if len(redirect_data) == 2:
                        print(f"Redirecting by type [{redirect_data[0]}] with selector [{redirect_data[1]}]")
                        if redirect_data[0] == "instance":
                            response = b"None"
                            for conn in self._connections:
                                if self._connections[conn]["instance_type"] == redirect_data[1]:
                                    response = (str(self._connections[conn]["address"][0]) + "$" +
                                                str(self._connections[conn]["port"])).encode("UTF-8")
                                    break
                            client_socket.send(response)
                        elif redirect_data[0] == "name":
                            if redirect_data[1] in self._connections:
                                client_socket.send((str(self._connections[redirect_data[1]]["address"][0]) + "$" +
                                                    str(self._connections[redirect_data[1]]["port"])).encode("UTF-8"))
                            else:
                                client_socket.send(b"None")
                        elif redirect_data[0] == "zone":
                            response = b"None"
                            for conn in self._connections:
                                if self._connections[conn]["zone"] == redirect_data[1]:
                                    response = (str(self._connections[conn]["address"][0]) + "$" +
                                                str(self._connections[conn]["port"])).encode("UTF-8")
                                    break
                            client_socket.send(response)
                    else:
                        client_socket.send(b"None")

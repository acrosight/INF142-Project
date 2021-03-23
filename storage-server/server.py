# TODO: import mongoLibrary from mongodb
from selectors import DefaultSelector, EVENT_READ
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import sys

# Listen for TCP and UDP connections

# On new data from stations, write data to mongodb


class Server:

    def __init__(self, host, port, server_type):

        if server_type =="TCP":
            self._sock = socket(AF_INET, SOCK_DGRAM)
            self._sock.bind(host, port)
            self._sock.listen(100)
        elif server_type == "UDP":
            self._sock = socket(AF_INET, SOCK_STREAM)
            self._sock.bind(host, port)
        
        self._sock.setblocking(False)
        self._server_type = server_type
        self._BUFFER_SIZE = 2048
        self._sel = DefaultSelector()
        self._sel.register(self._sock, EVENT_READ, self._recieve)

    def turn_on(self, sock):
        self._serving = True
        while self._serving:
            events = self._sel.select()
            for key, mask in events:
                functions = key.data
                functions(key.fileobj, mask)

    def shut_down(self):
        self._serving = False

    def _recieve(self, sock ,mask):
        if self._server_type == "TCP":
            conn,_ = sock.accept()
            conn.setBlocking(False)
            data = conn.recv(self._BUFFER_SIZE)
            ## For debugging
            conn.sendall("TCP data recived")
        else:
            data, _ = sock.recv(self._BUFFER_SIZE)
        if data:
            info = data.decode()
            print(info)
            ## Do something about the data recieved
            self.postToDB(data)
        else:
            self._sel.unregister(sock)
            conn.close()

    def postToDB(self, data):
        print("posting to DB")
    

if __name__ == "__main__":
    server = Server('localhost', 5550, str(sys.argv))
    server.turn_on(server)

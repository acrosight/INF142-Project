from pymongo import MongoClient
from selectors import DefaultSelector, EVENT_READ
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import sys

# Listen for TCP and UDP connections

# On new data from stations, write data to mongodb


class Server:

    def __init__(self, host, port, server_type):

        if server_type.upper() =="TCP":
            self._sock = socket(AF_INET, SOCK_STREAM)
            self._sock.bind((host, port))
            self._sock.listen(100)
        elif server_type.upper() == "UDP":
            self._sock = socket(AF_INET, SOCK_DGRAM)
            self._sock.bind((host, port))
        
        # self._sock.setblocking(False)
        self._server_type = server_type
        self._BUFFER_SIZE = 2048
        self._sel = DefaultSelector()
        self._sel.register(self._sock, EVENT_READ, self._recieve)

    def turn_on(self, sock):
        print("Turning on the server...")
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
            ## For debugging purposes,
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

    # Connect 
    def postToDB(self, data):
        # Connecting to MongoDB
        client = MongoClient(port=27017)
        db = client.weather
        # Creating sample from given data
        print(data)
        for x in data:
            report = {
                'rain': x['rain'],
                'temperature': x['temperature'],
                'day': x['day'],
            }
            ## Insert report into db
            result = db.reviews.insert_one(report)
        print(result)
        print("finished posting to MongoDB")
    

if __name__ == "__main__":
    udp_server = Server('localhost', 5550, 'UDP')
    tcp_server = Server('localhost', 5550, 'TCP')
    # server = Server('localhost', 5550, str(sys.argv))
    # server.turn_on(server)
    udp_server.turn_on(udp_server)
    tcp_server.turn_on(tcp_server)

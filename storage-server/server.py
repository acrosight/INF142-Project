import json
from pymongo import MongoClient
from selectors import DefaultSelector, EVENT_READ
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import sys
import os

# Listen for TCP and UDP connections

# On new data from stations, write data to mongodb
# Retrieves the variables necessary to assemble the MONGO URI
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
MONGODB_HOSTNAME = os.environ.get('MONGODB_HOSTNAME')
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE')

mongodb = f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}' \
        '@{MONGODB_HOSTNAME}:27017/{MONGODB_DATABASE}'

class Server:

    def __init__(self, host, port, server_type):

        if server_type.upper() =="TCP":
            print("Starting TCP server")
            self._sock = socket(AF_INET, SOCK_STREAM)
            self._sock.bind((host, port))
            self._sock.listen(100)
        elif server_type.upper() == "UDP":
            print("Starting UDP server")
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
            print('TCP recv')
            conn,_ = sock.accept()
            data = conn.recv(self._BUFFER_SIZE)
            ## For debugging purposes,
            conn.sendall("TCP data recived".encode())
        elif self._server_type == "UDP":
            print('UDP recv')
            data, _ = sock.recvfrom(self._BUFFER_SIZE)

        if data:
            info = data.decode()
            ## Do something about the data recieved
            self.postToDB(info)
        else:
            self._sel.unregister(sock)
            conn.close()
        
    # Connect 
    def postToDB(self, data):
        # Connecting to MongoDB
        print("Connecting to MongoDB")
        client = MongoClient(mongodb)
        db = client.weather
        # Creating sample from given data
        x = json.loads(data)
        print(x)

        report = {
            'temperature': x['temperature'],
            'precipitation': x['precipitation'],
            'location': x['location'],
        }
        print(report)
        ## Insert report into db
        result = db.reviews.insert_one(x)
        print(result)
        print("finished posting to MongoDB")
        return
    

if __name__ == "__main__":
    udp_server = Server('localhost', 5550, 'UDP')
    tcp_server = Server('localhost', 5555, 'TCP')
    # server = Server('localhost', 5550, str(sys.argv))
    # server.turn_on(server)
    udp_server.turn_on(udp_server)
    tcp_server.turn_on(tcp_server)

import json
from pymongo import MongoClient
from selectors import DefaultSelector, EVENT_READ
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import os

# Listen for TCP and UDP connections

# On new data from stations, write data to mongodb
# Retrieves the variables necessary to assemble the MONGO URI
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME', "root")
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', "example")
MONGODB_HOSTNAME = os.environ.get('MONGODB_HOSTNAME', "localhost")
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE', "weatherstation")
MONGODB_COLLECTION = os.environ.get('MONGODB_COLLECTION', "sensorData")
SERVER_TYPE = os.environ.get('SERVER_TYPE', 'UDP')

MONGODB_CONNECTIONSTRING = f'mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOSTNAME}:27017'
print(MONGODB_CONNECTIONSTRING)


def add_data_to_db(data: str):
    '''
    Add data to mongodb collection, data must be serializeable to a dictionary
    '''
    # Connecting to MongoDB
    print("Connecting to MongoDB")
    mydb = MongoClient(MONGODB_CONNECTIONSTRING)[MONGODB_DATABASE]
    mycol = mydb[MONGODB_COLLECTION]
    # Parse data from string to dictionary
    x = json.loads(data)
    print(x)

    report = {
        'temperature': x['temperature'],
        'precipitation': x['precipitation'],
        'location': x['location'],
        'timestamp': x['timestamp'],
    }
    print(report)
    # Insert report into db
    try:
        mycol.insert_one(x)
    except Exception as e:
        print("Failed to insert ", e)
    except KeyboardInterrupt:
        print("Interrupted by user")


class Server:
    '''
    General connection server for either udp or tcp connections.
    '''

    def __init__(self, server_type):
        if server_type.upper() == "TCP":
            print("Starting TCP server")
            self._sock = socket(AF_INET, SOCK_STREAM)
            self._sock.bind(('0.0.0.0', 5555))
            self._sock.listen(100)
            self._sock.setblocking(False)
        elif server_type.upper() == "UDP":
            print("Starting UDP server")
            self._sock = socket(AF_INET, SOCK_DGRAM)
            self._sock.bind(('0.0.0.0', 5550))

        self._sock.setblocking(False)
        self._server_type = server_type
        self._BUFFER_SIZE = 16128
        self._sel = DefaultSelector()
        self._sel.register(self._sock, EVENT_READ, self._recieve)

    def turn_on(self):
        print("Turning on the server...")
        self._serving = True
        try:
            while self._serving:
                events = self._sel.select()
                for key, mask in events:
                    functions = key.data
                    functions(key.fileobj, mask)
        except KeyboardInterrupt:
            print("Breaking due to keyboard interrupt")

    def shut_down(self):
        self._serving = False

    def _recieve(self, sock, mask):
        if self._server_type == "TCP":
            print('TCP recv')
            conn, _ = sock.accept()
            conn.setblocking(False)
            data = conn.recv(self._BUFFER_SIZE)
            # For debugging purposes,
            conn.sendall("TCP data recived".encode())
        elif self._server_type == "UDP":
            print('UDP recv')
            data, _ = sock.recvfrom(self._BUFFER_SIZE)

        if data:
            info = data.decode()
            # Do something about the data recieved
            try:
                add_data_to_db(info)
            except Exception as e:
                print("Failed to insert to mongodb", e)
        else:
            self._sel.unregister(sock)
            conn.close()


if __name__ == "__main__":
    print("Storage server starting", SERVER_TYPE)
    server = Server(SERVER_TYPE)
    server.turn_on()

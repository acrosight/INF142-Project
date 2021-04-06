from time import sleep
from station import StationSimulator
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import random
import json
import sys

def tcp_client(data):
    print("sending with tcp")
    socket_type = SOCK_STREAM
    sock = socket()
    
    sock.connect((address, port))
    print(f'Sending data {data}')
    sock.send(data.encode())
    server_answer = sock.recv(2048).decode()
    print(f"Answer from the server: {server_answer}")
    sock.close()


def udp_client(data):
    print("sending with udp")
    socket_type = SOCK_DGRAM
    sock = socket(address_fam, socket_type)


    print(f'Sending data {data}')
    sock.sendto(data.encode(), (address, port))
    
if __name__ == "__main__":

    # Instantiate a station simulator
    bergen_station = StationSimulator(simulation_interval=1)
    # Turn on the simulator
    bergen_station.turn_on()

    location = bergen_station.location

    address_fam = AF_INET
    address = "localhost"
    rand = random.randint(0, 1)

    while (True):
        # Sleep for 5 second to wait for new weather data
        # to be simulated
        sleep(5)
        # Read new weather data
        temperature = bergen_station.temperature
        precipitation = bergen_station.rain

        # Package data as json_string
        latest_data = json.dumps(
            {"temperature": temperature, "precipitation": precipitation, "location": location})

        port = 5555
        tcp_client(latest_data)
        
        break

        # if (rand):  # Randomly decide tcp or upd client
        #     port = 5555
        #     tcp_client(latest_data)
        # else:
        #     port = 5550
        #     udp_client(latest_data)
        # break

    # Shut down the simulation
    bergen_station.shut_down()






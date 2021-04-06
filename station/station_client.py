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
    print("Station client started")
    # Instantiate a station simulator
    cities = ["Alta","Arendal","Askim","Bergen","Bodø","Brekstad","Brevik","Brumunddal","Bryne","Brønnøysund","Drammen","Drøbak","Egersund","Elverum","Fagernes","Farsund","Fauske","Finnsnes","Flekkefjord","Florø","Fosnavåg","Fredrikstad","Førde","Gjøvik","Grimstad","Halden","Hamar","Hammerfest","Harstad","Haugesund","Hokksund","Holmestrand","Honningsvåg","Horten","Hønefoss","Jessheim","Jørpeland","Kirkenes","Kolvereid","Kongsberg","Kongsvinger","Kopervik","Kragerø","Kristiansand","Kristiansund","Langesund","Larvik","Leknes","Levanger","Lillehammer","Lillesand","Lillestrøm","Lyngdal","Mandal","Mo i Rana","Moelv","Molde","Mosjøen","Moss","Mysen","Måløy","Namsos","Narvik","Notodden","Odda","Orkanger","Oslo","Otta","Porsgrunn","Raufoss","Risør","Rjukan","Røros","Sandefjord","Sandnes","Sandnessjøen","Sandvika","Sarpsborg","Sauda","Ski","Skien","Skudeneshavn","Sortland","Stathelle","Stavanger","Stavern","Steinkjer","Stjørdalshalsen","Stokmarknes","Stord","Svelvik","Svolvær","Tromsø","Trondheim","Tvedestrand","Tønsberg","Ulsteinvik","Vadsø","Vardø","Verdalsøra","Vinstra","Åkrehamn","Ålesund","Åndalsnes","Åsgårdstrand"]
    
    curr_location = cities[random.randint(0, len(cities))]
    
    station = StationSimulator(location = curr_location, simulation_interval=1)
    # Turn on the simulator
    station.turn_on()

    location = station.location

    address_fam = AF_INET
    address = "localhost"

    try:
        while (True):
            # Sleep for 5 second to wait for new weather data
            # to be simulated
            sleep(5)
            # Read new weather data
            temperature = station.temperature
            precipitation = station.rain

            # Package data as json_string
            latest_data = json.dumps(
                {"temperature": temperature, "precipitation": precipitation, "location": location})

            rand = random.randint(0, 1)
            try:
                if rand:  # Randomly decide tcp or upd client
                    port = 5555
                    tcp_client(latest_data)
                else:
                    port = 5550
                    udp_client(latest_data)
            except Exception as e:
                print("Unable to post data", e)
    except KeyboardInterrupt:
        print("Breaking due to keyboard interrupt")

    # Shut down the simulation
    station.shut_down()

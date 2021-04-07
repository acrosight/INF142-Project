import os
from time import sleep
import datetime
from station import StationSimulator
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
import random
import json

RUNNING_IN_DOCKER = True if os.environ.get('RUNNING_IN_DOCKER') else False
print(f"Station running in docker: {RUNNING_IN_DOCKER}")


def tcp_client(data):
    address = "storage-server-tcp" if (RUNNING_IN_DOCKER) else "localhost"
    print(f"sending with tcp {data} to {address}")
    socket_type = SOCK_STREAM
    sock = socket(type=socket_type)

    sock.connect((address, 5555))
    sock.send(data.encode())
    server_answer = sock.recv(2048).decode()
    print(f"Answer from tcp server: {server_answer}")
    sock.close()


def udp_client(data):
    address = "storage-server-udp" if (RUNNING_IN_DOCKER) else "localhost"
    print(f"sending with udp {data} to {address}")
    address_fam = AF_INET
    socket_type = SOCK_DGRAM
    sock = socket(family=address_fam, type=socket_type)

    sock.sendto(data.encode(), (address, 5550))


def get_random_city():
    cities = ["Alta", "Arendal", "Askim", "Bergen", "Bodø", "Brekstad", "Brevik", "Brumunddal", "Bryne", "Brønnøysund", "Drammen", "Drøbak", "Egersund", "Elverum", "Fagernes", "Farsund", "Fauske", "Finnsnes", "Flekkefjord", "Florø", "Fosnavåg", "Fredrikstad", "Førde", "Gjøvik", "Grimstad", "Halden", "Hamar", "Hammerfest", "Harstad", "Haugesund", "Hokksund", "Holmestrand", "Honningsvåg", "Horten", "Hønefoss", "Jessheim", "Jørpeland", "Kirkenes", "Kolvereid", "Kongsberg", "Kongsvinger", "Kopervik", "Kragerø", "Kristiansand", "Kristiansund", "Langesund", "Larvik", "Leknes", "Levanger", "Lillehammer", "Lillesand",
              "Lillestrøm", "Lyngdal", "Mandal", "Mo i Rana", "Moelv", "Molde", "Mosjøen", "Moss", "Mysen", "Måløy", "Namsos", "Narvik", "Notodden", "Odda", "Orkanger", "Oslo", "Otta", "Porsgrunn", "Raufoss", "Risør", "Rjukan", "Røros", "Sandefjord", "Sandnes", "Sandnessjøen", "Sandvika", "Sarpsborg", "Sauda", "Ski", "Skien", "Skudeneshavn", "Sortland", "Stathelle", "Stavanger", "Stavern", "Steinkjer", "Stjørdalshalsen", "Stokmarknes", "Stord", "Svelvik", "Svolvær", "Tromsø", "Trondheim", "Tvedestrand", "Tønsberg", "Ulsteinvik", "Vadsø", "Vardø", "Verdalsøra", "Vinstra", "Åkrehamn", "Ålesund", "Åndalsnes", "Åsgårdstrand"]

    return cities[random.randint(0, len(cities))]


if __name__ == "__main__":
    print("Station client started")
    # Instantiate a station simulator
    station = StationSimulator(
        location=get_random_city(), simulation_interval=1)
    # Turn on the simulator
    station.turn_on()

    location = station.location

    try:
        while (True):
            # Read new weather data
            temperature = station.temperature
            precipitation = station.rain

            # Package data as json_string
            latest_data = json.dumps(
                {
                    "temperature": temperature,
                    "precipitation": precipitation,
                    "location": location,
                    'timestamp': str(datetime.datetime.now())
                })

            # Randomly use tcp or udp to send package
            rand = random.randint(0, 1)
            try:
                if rand:
                    tcp_client(latest_data)
                else:
                    udp_client(latest_data)
            except Exception as e:
                print("Unable to post data", e)

            # Sleep for 5 second to wait for new weather data
            # to be simulated
            sleep(5)
    except KeyboardInterrupt:
        print("Breaking due to keyboard interrupt")

    finally:
        # Shut down the simulation
        station.shut_down()

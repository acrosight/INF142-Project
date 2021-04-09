# INF142-Project - Group 31

Mandatory assignment 2 - Group 31

## Proposal

![Proposal for architecture](Architecture-proposal.png)

- Station client, randomly using UDP / TCP
- Storage server accepting UDP and TCP connections
- MongoDB for storing sensor data
- WebServer for rendering the web page displaying sensor data from MongoDB
- Frontend with some simple Javascript code for fetching data from the server.

## Run all containers:

1. `docker-compose up`
2. Visit `localhost:5000` in browser
3. Success

#### Build new docker images after code modifications:

1. Close current running docker-compose by either interrupting the terminal or `docker-compose down`
2. Delete old docker images: `docker image rm web-server storage-server station -f`
3. Rebuild and start: `docker-compose up`
4. Answer `y` when asked to replace old containers

## Getting started with web-server (local)

1.  Run the following command in the root folder:

    `pip install -r requirements.txt`.

2.  Set up a .env file with the following variables in the web-server folder:

    - APP_PORT
    - MONGODB_DATABASE
    - MONGODB_USERNAME
    - MONGODB_PASSWORD
    - MONGODB_HOSTNAME

3.  Run the following command `python server.py` in the web-server folder to
    start the server.

## MVP
 - [X]  It  consists  of  at  least  three  Python  scripts,  one  for  each  of  the  aforementionedprocesses.
 - [X]  At least one TCP socket is used.
 - [X]  At least one UDP socket is used.
 - [X]  The provided script station.py is used by the weather station process to simulate the readings of weather sensors. Note that you only need to import a class from this script. You do not need to understand the code in it.
 - [X]  The storage server process periodically stores data in a file or database.
 - [X]  The storage server process provides remote access to the stored data.
 - [X]  The FMI process(user agent) runs in a CLI and, upon request, displays all the data available in the storage server.

## Adding some extras

- [] Requests
- [X] Flask
- [X] Docker (and Docker Compose)
- [] SQL
- [X] MongoDB
- [X] A GUI

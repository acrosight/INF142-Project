# INF142-Project

Mandatory assignment 2

## Proposal

![Proposal for architecture](Architecture-proposal.png)

- Station client, randomly using UDP / TCP
- Storage server accepting UDP and TCP connections
- MongoDB for storing sensor data
- WebServer for serving frontend and serving REST API for reading sensor data from MongoDB
- Frontend with some simple Javascript code for fetching data from REST API

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

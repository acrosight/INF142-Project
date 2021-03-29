# INF142-Project

Mandatory assignment 2

## Proposal

![Proposal for architecture](Architecture-proposal.png)

- Station client, randomly using UDP / TCP
- Storage server accepting UDP and TCP connections
- MongoDB for storing sensor data
- WebServer for serving frontend and serving REST API for reading sensor data from MongoDB
- Frontend with some simple Javascript code for fetching data from REST API

## Getting started

1.  Install the required modules (in a virtualenv) by running
    `pip install -r requirements.txt`.

2.  Start MongoDB from command line by running `mongo` (Requires that MongoDB is installed).

3.  Start the web server by running server.py in the web-server folder.

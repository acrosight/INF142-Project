# INF142-Project

Mandatory assignment 2

## Proposal

![Proposal for architecture](Architecture-proposal.png)

- Station client, randomly using UDP / TCP
- Storage server accepting UDP and TCP connections
- MongoDB for storing sensor data
- WebServer for serving frontend and serving REST API for reading sensor data from MongoDB
- Frontend with some simple Javascript code for fetching data from REST API

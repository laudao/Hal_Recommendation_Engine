# Recommendation engine for HAL articles

A search and recommendation engine built on topic extraction from [HAL](https://hal.archives-ouvertes.fr/) archives.
## Stack
  - Neo4j-Server
  - Cypher
  - Bottle
  - Frontend: jquery, bootstrap, d3.js
  
## Setup
Install the dependencies for the app:
`$ pip install -r requirements.txt`

## Run locally
Start your Neo4j Server : [Download & Install](https://neo4j.com/download/)

Then start up a Bottle Web Server :
`$ python example.py`

Finally, navigate to http://localhost:8080 to see the application.

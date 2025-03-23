# Sentim*ai*l API Server
## Description
This is a basic API that returns gets data from a postgres DB.

## Running the server
To run the server locally you need to add an .env file with the following properties
```
# Server
PORT=

# DB
DB_HOST=
DB_PORT=
DB_NAME=
DB_USER=
DB_PASSWORD=
```
You can than run the server using the following command
```
node .\index.js
```

## Expanding the API
If you want to add endpoints to the API here is how to do it.

### SQL
Add relevant sql files to the proper SQL folder.

### Service
create a new service or add functions to an existing service. 
Each servise is normally for each SQL folder.
In the service add inner SQL folder logic (such as using 2 SQL files from the same folder).

### Controller
create a new controller or add functions to an existing service. 
Each controller is normally for each service but can combine multiple services.
In the controller add logic that uses multiple services.

### Route
create a new route or add functions to an existing service.
The route create URL endpoints to each controller.

### Index
In the index file add the route if needed and add its basic endpoint


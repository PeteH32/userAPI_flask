# UserAPI - A rest resource for users and exams, implemented in Python/Flask

- [UserAPI - A rest resource for users and exams, implemented in Python/Flask](#userapi---a-rest-resource-for-users-and-exams--implemented-in-python-flask)
  * [Prerequisites](#prerequisites)
  * [Build and run](#build-and-run)
  * [The Rest API](#the-rest-api)
    + [Format: JSON:API specification](#format--json-api-specification)
    + [Security](#security)
    + [API Endpoints](#api-endpoints)
  * [Cleanup](#cleanup)

## Prerequisites

Everything runs inside a Docker container, so you do not need to have Python3 
or pip on your OSX machine. You just need Docker.

- Mac OSX is what I tested on, but should also work on Windows 10 and Linux.
- Install Docker and Docker-Compose

## Build and run

- Build and run the service:
  - NOTE: Must manually start the postgres db before starting the restapp.
    - `docker-compose up -d db`
    - `docker-compose up -d restapp`
- Shutdown service:
  - `docker-compose down`
- Re-build after making code changes:
  - `docker-compose build`
  - NOTE: I have not yet mounted the "src" folder, which would then allow code changes to be picked up live, without rebuilding/restarting.
- Check if service is running:
  - `docker ps -l`
  - `docker ps -la`
- Tail the logs:
  - `docker logs -tf userapi_flask_restapp_1`
- To "ssh" into the running service (not really ssh):
  - `docker exec -it userapi_flask_restapp_1 sh -l`

## The Rest API

### Format: JSON:API specification

The Users/Exams Rest API fully implements the JSON:API specification (v1.0);

- https://jsonapi.org/format

### Security

WARNING:

- Currently there is no authentication.

### API Endpoints

The UserAPI service's container is mapped to port 5000 on your local OSX.

In addition to the "users" endpoint, I also added an "exams" endpoint to demonstrate relationships in JSON:API.

- Users endpoint
  - `curl http://127.0.0.1:5000/users`
- Exams endpoint
  - `curl http://127.0.0.1:5000/exams`

## Cleanup

To cleanup all docker images, containers, etc:

- `docker-compose down`
- `docker image rm user_api_flask`
- WARNING: This next step is will remove ALL unused images from your machine, not just the ones from this project. It is optional.
  - `docker image prune -f`
- `docker volume rm userapi_flask_user-api-data`

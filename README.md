# A User rest resource, implemented using Python and Flask

## Prerequisites

Everything runs inside a Docker container, so you do not need to have Python3 
or pip on your OSX machine. You just need Docker.

- Mac OSX. That's what I tested on, but should also work on Windows 10 and Linux.
- Install Docker and Docker-Compose

## Build and run

- Build and run the service:
  - `docker-compose up -d`
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
- To "ssh" into the service (not really ssh):
  - `docker exec -it userapi_flask_restapp_1 sh -l`

## Cleanup

To cleanup all docker images, containers, etc:

- `docker-compose down`
- `docker image rm user_api_flask`
- WARNING: This next step will remove ALL unused images from your machine, not just the ones form this project.
  - `docker image prune -f`

## The Rest API

### Rest format using JSON:API specification

This Rest API fully implements the JSON:API specification (v1.0);

- https://jsonapi.org/format

### Security

WARNING: Currently there is no authentication.

### API Endpoints

The service's container is mapped to port 5000 on your local OSX.

In addition to the "users" endpoint, I also added an "exams" endpoint to demonstrate relationships.

- Users endpoint
  - `curl http://127.0.0.1:5000/users`
- Exams endpoint
  - `curl http://127.0.0.1:5000/exams`

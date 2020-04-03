# A User rest resource, implemented using Python and Flask

## Prerequisites

This is what I tested on. Everything runs inside a Docker container, so you do not need to have Python3 
or pip on your OSX machine. You just need Docker.

- Mac OSX
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

The service's container is mapped to port 5000 on your local OSX.

NOTE: Currently there is no authentication.

- Users endpoint
  - `curl http://127.0.0.1:5000/users`
- Exams endpoint
  - `curl http://127.0.0.1:5000/exams`

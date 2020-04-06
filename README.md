# UserAPI - A rest resource for users and exams, implemented in Python/Flask

- [UserAPI - A rest resource for users and exams, implemented in Python/Flask](#userapi---a-rest-resource-for-users-and-exams--implemented-in-python-flask)
  * [Description](#description)
  * [Prerequisites](#prerequisites)
  * [Build and run](#build-and-run)
  * [The Rest API](#the-rest-api)
    + [Format: JSON:API specification](#format--json-api-specification)
    + [Security](#security)
    + [API Endpoints](#api-endpoints)
      - [Background](#background)
      - [API Documentation](#api-documentation)
  * [Automated tests](#automated-tests)
  * [Cleanup](#cleanup)

## Description

A full JSON:API rest client, backed by a Postgres database. Implements following two API endpoints:

- `/users` - Users
- `/exams` - Exams, added so can show relationships. A "user" can have many "exams".

## Prerequisites

Everything runs inside a Docker container, so you do not need to have Python3 
or pip on your OSX machine. You just need Docker.

- Mac OSX is what I tested on, but should also work on Windows 10 and Linux.
- Install Docker and Docker-Compose

## Build And Run

- Build and run the service:
  - `make up`
- Shutdown service:
  - `make down`
- Run automated tests
  - See below section "Automated Tests"
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

#### Background

The UserAPI service's container is mapped to port 5000 on your local OSX.

In addition to the "users" endpoint, I also added an "exams" endpoint to demonstrate relationships in JSON:API.

- Users endpoint
  - `curl http://127.0.0.1:5000/users`
- Exams endpoint
  - `curl http://127.0.0.1:5000/exams`

#### API Documentation

I generated API doc here:

- Note: All CRUD operations work per JSON:API spec (v1.0): https://jsonapi.org/format
- Note: It's best to directly open this web page in Chrome
  - ./docs/Bright.MD_API.html

## Automated Tests

Although this is a full JSON:API rest client backed by a Postgres database, there is almost no business-logic in this 
codebase (it's basically a simple I/O app). In this scenario I think that, instead of unit tests, it's more effective to use Rest API tests. I used Postman and Newman to create these tests.

To run the automated API tests:

- Recommended to start with fresh (empty) database
  - `make delete_db`
- Run the API tests:
  - `make runtests`
  - In the test output, all API calls should return success:
    - "200 OK"
    - "201 CREATED"
- Newman has ability to provide assertions and verify that each API call is returning expected values, including 
expected errors. But I do not know Newman enough yet to write Newman assertions/checks. This is just the groundwork for those tests.

## Cleanup

To cleanup all docker images, containers, etc:

- `make clean`

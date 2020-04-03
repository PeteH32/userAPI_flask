FROM python:3.7-alpine

# Need these in order to install Python dependency "psycopg2" which needs built from source code.
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# First, only do dependencies, so they're in their own docker cache layer. This is so when we make code changes,
# the "docker build" will not need to redo "pip install" (you'll see "Using cache" for that step).
COPY src/requirements.txt /myapp/
RUN pip install -U pip
RUN pip install -r /myapp/requirements.txt

# Copy all src files.
COPY src /myapp

# Copy scripts
COPY scripts/docker_entrypoint.sh /
RUN chmod u+x /docker_entrypoint.sh
COPY scripts/.aliases /root/.profile

WORKDIR /myapp
CMD ["/docker_entrypoint.sh"]

EXPOSE 5000

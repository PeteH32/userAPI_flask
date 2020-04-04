
up:
	docker-compose up -d db
	# Note: Pausing to let "db" get it's port open, before we start "restapp". This is the hacky way to do it.
	sleep 3
	docker-compose up -d restapp

down:
	docker-compose down

runtests:
	# To see Newman command-line help:
	#	docker run --rm -it postman/newman:4.6.0-alpine run -h
	docker run --rm -v="${PWD}/tests/postman_collections:/etc/newman" --network="userapi_flask_default" postman/newman:4.6.0-alpine run "Bright.MD API.postman_collection.json"

runtests_cli:
	# To see Newman command-line help:
	#	docker run --rm -it postman/newman:4.6.0-alpine run -h
	docker run --rm -v="${PWD}/tests/postman_collections:/etc/newman" --network="userapi_flask_default" postman/newman:4.6.0-alpine run "Bright.MD API.postman_collection.json" -r cli

runtests_json:
	# To see Newman command-line help:
	#	docker run --rm -it postman/newman:4.6.0-alpine run -h
	docker run --rm -v="${PWD}/tests/postman_collections:/etc/newman" --network="userapi_flask_default" postman/newman:4.6.0-alpine run "Bright.MD API.postman_collection.json" -r json --reporter-json-export newman-report.json

delete_db:
	docker-compose down
	docker volume rm userapi_flask_user-api-data
	docker ps -a
	docker volume ls

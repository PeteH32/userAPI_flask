
up:
	docker-compose up -d db
	# Note: Cannot let "restapp" try to connect to "db" before the db has it's port open and ready. So doing a hack-y sleep.
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

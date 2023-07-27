# for start mySQL container:
rundb:
	docker compose -f infra/dev/docker-compose.local.yaml up -d

# for stop mySQL container:
stopdb:
	docker compose -f infra/dev/docker-compose.local.yaml down

# for stop mySQL container and delete database:
deletedb:
	docker compose -f infra/dev/docker-compose.local.yaml down --volumes

# for start bot with Database container:
runbot-db:
	docker compose -f infra/dev/docker-compose.local.yaml up -d
	cd src && poetry run uvicorn config.asgi:application --reload && cd ..

filldb:
	python src/utils/db_fixtures/filldb.py

# To generate factories with coordinators info use command:
# 'make generate_contacts amount=5', where 'amount' is <int> value
# of factories you want to generate, e.g. 5.
generate_contacts:
	python src/db_fixtures/factories/contact_factories.py ${amount}

# for start mySQL container:
rundb:
	docker compose -f infra/dev/docker-compose.local.yaml up -d

# for stop mySQL container:
stopdb:
	docker compose -f infra/dev/docker-compose.local.yaml down

# for stop mySQL container and delete database:
deletedb:
	docker compose -f infra/dev/docker-compose.local.yaml down --volumes

# for start bot with mySQL container:
runbot-db:
	docker compose -f infra/dev/docker-compose.local.yaml up -d
	python src/run_bot.py

filldb:
	python src/db_fixtures/filldb.py


APP_NAME ?= restaurant-api

default: run

run:
	docker-compose up -d

build: prune
	docker-compose build

stop:
	docker-compose down

logs:
	docker-compose logs -f

run-with-logs: run logs

cli:
	docker-compose run --rm cli bash

shell:
	docker-compose run --rm cli python manage.py shell

migrate:
	docker-compose run --rm cli python manage.py migrate

makemigrations:
	docker-compose run --rm cli python manage.py makemigrations

prune:
	docker-compose down -v --remove-orphans --rmi local

dumpdata:
	docker-compose run --rm cli python manage.py dumpdata > fixtures/initial_data.json

loaddata:
	docker-compose run --rm cli python manage.py loaddata fixtures/initial_data.json

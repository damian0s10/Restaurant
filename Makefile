
APP_NAME ?= restaurant-api

default: run

run:
	docker-compose up -d

build:
	docker-compose build

rebuild: prune build

stop:
	docker-compose down

logs:
	docker-compose logs -f

run-with-logs: run logs

cli:
	docker-compose run --rm web bash

shell:
	docker-compose run --rm web python manage.py shell

migrate:
	docker-compose run --rm web python manage.py migrate

makemigrations:
	docker-compose run --rm web python manage.py makemigrations

prune:
	docker-compose down -v --rmi local --remove-orphans

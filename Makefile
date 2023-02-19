build:
	poetry build

install:
	poetry install

lint:
	poetry run flake8 page_analyzer

test:
	poetry run pytest

coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

check: lint test

build-db: db-drop db-create schema-data-load

db-start:
	sudo service postgresql start

db-status:
	sudo service postgresql status

db-stop:
	sudo service postgresql stop

db-create:
	createdb page_analyzer

db-drop:
	dropdb page_analyzer

db-reset:
	dropdb page_analyzer || true
	createdb page_analyzer

db-dev-setup: db-reset schema-load

schema-load:
	psql page_analyzer < database.sql

db-connect:
	psql -d page_analyzer

dev:
	poetry run flask --app page_analyzer:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
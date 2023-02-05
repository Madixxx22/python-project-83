build:
	poetry build

install:
	poetry install

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 page_analyzer

test:
	poetry run pytest

make coverage:
	poetry run pytest --cov=gendiff --cov-report xml

make check: lint test coverage

dev:
	poetry run flask --app page_analyzer:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
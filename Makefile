install:
	uv sync

build:
	./build.sh

makemigrations:
	uv run manage.py makemigrations

migrate:
	uv run manage.py migrate

tailwind-build:
	uv run manage.py tailwind build --force

compilemessages:
	uv run manage.py compilemessages --locale ru --ignore=.venv --verbosity 0

collectstatic: tailwind-build compilemessages
	uv run manage.py collectstatic --noinput

start:
	uv run manage.py runserver

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check .

test:
	uv run manage.py test --settings=task_manager.test_settings

check: lint test

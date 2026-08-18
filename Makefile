install:
	uv sync

build:
	./build.sh

migrate:
	uv run manage.py migrate

compilemessages:
	uv run manage.py compilemessages --locale ru --ignore=.venv --verbosity 0

tailwind-build:
	uv run manage.py tailwind build --force

collectstatic: tailwind-build compilemessages
	uv run manage.py collectstatic --noinput

start:
	uv run manage.py runserver

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check .

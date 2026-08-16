install:
	uv sync

build:
	./build.sh

collectstatic:
	uv run manage.py collectstatic --noinput

migrate:
	uv run manage.py migrate

start:
	uv run manage.py runserver

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check .

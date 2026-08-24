### Hexlet tests and linter status:

[![Actions Status](https://github.com/apriakhin/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/apriakhin/python-project-52/actions)
[![CI Status](https://github.com/apriakhin/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/apriakhin/python-project-52/actions/workflows/pyci.yml)

# Task Manager

Task Manager is a Django web application for creating and tracking tasks. It
supports user accounts, task statuses, labels, executors, and filtering. Only a
task author can delete their task.

The deployed application is available at
[python-project-52-0wbl.onrender.com](https://python-project-52-0wbl.onrender.com).

## Install

Python 3.13 and [uv](https://docs.astral.sh/uv/) are required. PostgreSQL is
needed for a production-like local setup; SQLite is used by default.

Copy and run the commands below in the terminal:

```sh
git clone https://github.com/apriakhin/python-project-52.git
cd python-project-52
make install
```

Create a local environment file and set the required variables:

```sh
cp .env.example .env
```

```sh
export SECRET_KEY=your-secret-key
export DATABASE_URL=postgresql://user:password@localhost:5432/task_manager
export SENTRY_DSN=https://public-key@your-project.bugsink.com/project-id
```

Apply migrations, build static assets, and start the development server:

```sh
make migrate
make collectstatic
make start
```

## Usage

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser and register
an account. After signing in, create statuses and labels, then add tasks with a
status, executor, and optional labels. Use the task list filters to find tasks
by status, executor, label, or author.

## Error tracking

Unhandled errors are sent to Bugsink through Sentry SDK when `SENTRY_DSN` is
set. Configure the same environment variable in Render before deploying. The
DSN is secret and must not be committed to the repository.

FROM python:3.11.4-buster

RUN apt-get update

ENV PATH="/root/.local/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app/todo_app
COPY pyproject.toml poetry.lock /app/todo_app/

RUN poetry install --without dev
COPY todo_app todo_app

ENTRYPOINT poetry run gunicorn --bind 0.0.0.0:80 "todo_app.app:create_app()"

FROM python:3.11.4-buster as base

# Perform common operations, dependnecy installations etc...

RUN apt-get update

ENV PORT=80
EXPOSE $PORT
ENV PATH="/root/.local/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app/todo_app
COPY pyproject.toml poetry.lock /app/todo_app/

FROM base as production

# Configure for production

RUN poetry install --without dev
COPY todo_app todo_app

ENTRYPOINT poetry run gunicorn --bind 0.0.0.0:80 "todo_app.app:create_app()"

FROM base as development

RUN poetry install
ENTRYPOINT poetry run flask run --host=0.0.0.0 --port=$PORT

# Configure for development

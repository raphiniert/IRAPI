FROM python:3.11-alpine as base

ARG PROJECT_NAME irserver

# configure poetry
ENV POETRY_VERSION=1.4.2
ENV POETRY_HOME=/opt/poetry

# install poetry
RUN pip install pip --upgrade
RUN pip install poetry==${POETRY_VERSION}
RUN poetry config virtualenvs.create false

# switch to main work directory
WORKDIR /srv/$PROJECT_NAME

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

FROM base as dev
# install including dev dependencies
RUN poetry install

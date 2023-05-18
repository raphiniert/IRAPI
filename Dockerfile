FROM python:3.11-alpine as base

ARG PROJECT_NAME irserver

# set environment variables
# prevent python from writing *.pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# prevent python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

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
RUN poetry install --without test
ENTRYPOINT [ "/bin/sh", "start.sh" ]

FROM base as test
# install main and test dependencies
RUN poetry install --only main,test
ENTRYPOINT [ "/bin/sh", "start.sh" ]

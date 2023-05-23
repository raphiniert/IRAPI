[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
![code style](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)

# IRServer

fastapi server receiving, managing and sending ir signals

## Project structure

    .
    ├── api                       # fastapi app
    │   ├── core                  # core config
    │   │   ├── config.py         # load settings from .env
    │   │   └── security.py       # load keys, create tokens
    │   ├── crud                  # crud operations
    │   │   ├── devices.py        # device crud operations
    │   │   ├── signals.py        # signal crud operations
    │   │   └── users.py          # user crud operations
    │   ├── db                    # database
    │   │   └── models.py         # db models
    │   ├── routers               # object endpoints
    │   │   ├── auth.py           # auth endpoints
    │   │   ├── devices.py        # device endpoints
    │   │   ├── signals.py        # signal endpoints
    │   │   └── users.py          # user crud operations
    │   ├─- __init__.py           # create and config app
    │   ├─- database.py           # create async db session
    │   └─- schemes.py            # pydantic schemes
    ├── test                      # fastapi app
    │   ├── auth                  # auth tests
    │   ├── routes                # route tests
    │   └─- conftest.py           # setup fixutres
    ├── .env                      # environment variables
    ├── .gitignore                # .gitignore file
    ├── .pre-commit-config.yml    # pre commit config
    ├── compose.yml               # docker compose fastpi and postgres
    ├── Dockerfile                # py3.11 alpine base image
    ├── IRServer.code-worksapce   # vscode workspace
    ├── poetry.lock               # poetry lockfile
    ├── pyproject.toml            # dependencies and settings
    ├── README.md                 # this readme file
    └── start.sh                  # run uvicorn


## Setup

### Clone repo
```shell script
git clone https://github.com/raphiniert/irapi.git
cd irapi
```

### Create virtual env
```shell script
python3 -m venv venv
. venv/bin/activate
pip install pip --upgrade
pip install poetry
```

### Create .env file

```env
# project specific
PROJECT_NAME=irapi

# Postgres
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=replace-w/-very-secure-password
POSTGRES_DB=irapi
POSTGRES_PORT=5432

# authentication
# run: openssl genpkey -algorithm ed25519 -out private_key.pem
PASETO_PRIVATE_KEY="conent of private_key.pem"
# run: openssl pkey -in private_key.pem -pubout -out public_key.pem
PASETO_PUBLIC_KEY="content of public_key.pem"
ACCESS_TOKEN_EXPIRE_SECONDS=3600

# timezone
TZ=Europe/Vienna
```


#### Local dev

```shell script
docker coompose up -d  # start
docker compose down    # stop
docker compose logs -f # follow log output
```

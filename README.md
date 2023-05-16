# IRServer

fastapi server receiving, managing and sending ir signals

## Project structure

    .
    ├── api                       # fastapi app
    │   ├── core                  # core config
    │   │   └── config.py         # load settings from .env
    │   ├── crud                  # crud operations
    │   │   ├── devices.py        # device crud operations
    │   │   └── signals.py        # signal crud operations
    │   ├── db                    # database
    │   │   └── models.py         # db models
    │   ├── routers               # object endpoints
    │   │   ├── devices.py        # device endpoints
    │   │   └── signals.py        # signal endpoints
    │   ├─- __init__.py           # create and config app
    │   ├─- database.py           # create async db session
    │   └─- schemes.py            # pydantic schemes
    ├── .env                      # environment variables
    ├── .gitignore                # .gitignore file
    ├── .pre-commit-config.yml    # pre commit config
    ├── compose.yml               # docker compose fastpi and postgres
    ├── Dockerfile                # py3.11 alpine base image
    ├── poetry.lock               # poetry lockfile
    ├── pyproject.toml            # dependencies and settings
    ├── README.md                 # this readme file
    └── start.sh                  # run uvicorn


## Setup

### Clone repo
```shell script
git clone https://github.com/raphiniert/irserver.git
cd irserver
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
PROJECT_NAME=irserver

# Postgres
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=replace-w/-very-secure-password
POSTGRES_DB=irserver
POSTGRES_PORT=5432

# timezone
TZ=Europe/Vienna
```


#### Local dev

```shell script
docker coompose up -d  # start
docker compose down    # stop
docker compose logs -f # follow log output
```

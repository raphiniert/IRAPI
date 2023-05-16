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
│   │   └── models.py         # define db models
│   ├── routers               # object endpoints
│   │   ├── devices.py        # device endpoints
│   │   └── signals.py        # signal endpoints
│   ├─- __init__.py           # create and config app
│   ├─- database.py           # create async db session
│   └─- schemes.py            # pydantic schemes
├── .env                      # environment variables
├── .gitignore                # .gitignore file
├── .pre-commit-config.yml    # pre commit config
├── pyproject.toml            # .gitignore file
└── README.md                 # this readme file


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

#### Local dev

```shell script
poetry install
```

# IRServer

fastapi server receiving, managing and sending ir signals

## Project structure

.
├── api                       # fastapi app
│   ├── routers               # endpoints
│   │   └── signals.py        # signal endpoints
│   └─- __init__.py           # create and config app
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

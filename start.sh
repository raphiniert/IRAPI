#!/bin/sh
poetry run uvicorn api:create_app --factory --reload --host 0.0.0.0 --port 8000

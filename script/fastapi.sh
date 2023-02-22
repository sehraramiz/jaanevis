#!/bin/bash

set -e

sh script/prestart.sh
${PYTHONPATH:-python} -m poetry install
${PYTHONPATH:-python} -m uvicorn jaanevis.api.fastapi.main:app --reload --port ${PORT:-8000}

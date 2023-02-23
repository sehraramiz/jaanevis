#!/bin/bash

set -e

${PYTHONPATH:-python} -m poetry install
sh script/prestart.sh
${PYTHONPATH:-python} -m uvicorn jaanevis.api.fastapi.main:app --reload --port ${PORT:-8000}

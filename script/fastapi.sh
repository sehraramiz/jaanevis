#!/bin/bash

python -m uvicorn jaanevis.api.fastapi.main:app --reload --port ${PORT:-8000}

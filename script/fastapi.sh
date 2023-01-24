#!/bin/bash

uvicorn jaanevis.api.fastapi.main:app --reload --port ${PORT:-8000}

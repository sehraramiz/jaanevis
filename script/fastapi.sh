#!/bin/bash

uvicorn jaanevis.api.fastapi.main:app --reload --port 8000

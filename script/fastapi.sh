#!/bin/bash

uvicorn geonotes.api.fastapi.main:app --reload --port 8000

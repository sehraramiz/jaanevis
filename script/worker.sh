#!/bin/bash

SCRIPT_DIR=$( dirname -- "$0"; )
BASE_DIR="$(dirname "${SCRIPT_DIR}")"
${PYTHONPATH:-python} ${BASE_DIR}/jaanevis/tasks/core.py

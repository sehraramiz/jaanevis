#!/bin/sh -e
set -x

ruff jaanevis --fix
black jaanevis
isort jaanevis

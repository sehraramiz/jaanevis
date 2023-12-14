#!/bin/sh -e

set -x

ruff jaanevis --fix
isort jaanevis
black jaanevis

#!/bin/sh -e
set -x

ruff geonotes --fix
black geonotes
isort geonotes

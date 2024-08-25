#!/usr/bin/env bash
# exit on error

set -o errexit 

poetry install

# Set environment variable to disable collectstatic
# python manage.py collectstatic --no-input
export DISABLE_COLLECTSTATIC=1
export DEBUG="False"

python manage.py migrate
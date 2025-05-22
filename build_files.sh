#!/bin/bash

# Install dependencies
pip install -r requirements.txt
mkdir -p staticfiles_build
python manage.py collectstatic --noinput --clear --verbosity 0
python manage.py migrate

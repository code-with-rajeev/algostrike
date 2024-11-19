#!/bin/bash

#Install dependencies
pip install -r requirements.txt

#collect the static files
python manage.py collectstatic --noinput
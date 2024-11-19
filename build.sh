#!/bin/bash

#Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

#collect the static files
python manage.py collectstatic
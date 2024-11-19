#!/bin/bash

#Install dependencies
pip install -r requirements.txt

#collect the static files
python3.11 manage.py collectstatic
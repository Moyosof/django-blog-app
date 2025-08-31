#!/usr/bin/env bash

set -o errexit # Exit on error 

pip install -r requirement.txt # Install dependencies from requirements.txt file 

python manage.py collectstatic --noinput # Collect static files. 
python manage.py migrate # Apply database migrations.

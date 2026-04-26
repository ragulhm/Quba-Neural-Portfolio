#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

PYTHONPATH=. python manage.py collectstatic --no-input
PYTHONPATH=. python manage.py migrate
PYTHONPATH=. python portfolio/scripts/extract_knowledge.py
PYTHONPATH=. python ingest_data.py

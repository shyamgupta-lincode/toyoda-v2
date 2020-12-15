#!/bin/sh
python manage.py runserver 164.52.194.78:8000 &
celery -A livis.celery worker --loglevel=info &
python /root/freedom/backend/LIVIS/livis/annotate/extract -m http.server 3306 &

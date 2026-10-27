#!/usr/bin/env bash
# Выходим, если команда завершилась с ошибкой
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
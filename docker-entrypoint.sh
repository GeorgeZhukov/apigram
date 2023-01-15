#!/bin/bash -x

python manage.py collectstatic --no-input || exit 1
python manage.py migrate --no-input || exit 1

exec "$@"
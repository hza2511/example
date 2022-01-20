#!/bin/sh

sleep 30

python manage.py flush --no-input
python manage.py migrate
python manage.py migrate --schema=tenant_base_schema_template
python manage.py collectstatic --no-input --clear

exec "$@"

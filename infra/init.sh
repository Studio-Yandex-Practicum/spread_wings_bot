#!/bin/bash
docker-compose run bot python manage.py migrate
docker-compose run bot python manage.py collectstatic --noinput
docker-compose run bot python manage.py createsuperuser --email example@yandex.ru --noinput

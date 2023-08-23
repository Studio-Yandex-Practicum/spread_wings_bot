#!/bin/bash
docker exec -it spread-wings-bot python manage.py migrate
docker exec -it spread-wings-bot python manage.py collectstatic --noinput
docker exec -it spread-wings-bot python manage.py createsuperuser --email example@yandex.ru --noinput

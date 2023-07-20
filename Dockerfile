FROM python:3.11-slim

WORKDIR /app

COPY ./ /app

COPY ./requirements/develop.txt /app

RUN pip install --upgrade pip

RUN pip install -r ./requirements/develop.txt

WORKDIR ./src

CMD [ "uvicorn", "config.asgi:application" ]

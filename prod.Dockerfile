FROM python:3.11-slim

WORKDIR /app

COPY ./ /app

COPY ./requirements/production.txt /app

RUN pip install --upgrade pip

RUN pip install -r ./requirements/production.txt

WORKDIR ./src

CMD [ "uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000" ]

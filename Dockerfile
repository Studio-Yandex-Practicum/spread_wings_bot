FROM python:3.11-slim

WORKDIR /app

COPY ./ /app

COPY ./requirements/develop.txt /app

RUN apt-get update
RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv
RUN pip install --upgrade pip
RUN pip install -r ./requirements/develop.txt

ENV TELEGRAM_TOKEN ${TELEGRAM_TOKEN}
ENV DEBUG ${DEBUG}
ENV DB_URL ${DB_URL}

CMD [ "python", "./src/run_bot.py" ]
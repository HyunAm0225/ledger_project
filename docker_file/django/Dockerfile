FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  && pip install --upgrade pip

COPY ./docker_file/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

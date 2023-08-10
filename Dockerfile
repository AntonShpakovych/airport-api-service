FROM python:3.9-slim

LABEL maintainer="a.shpakovych.work@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc

RUN pip install -r requirements.txt

COPY . .


RUN adduser \
         --disabled-password \
         --no-create-home\
         django-user

USER django-user

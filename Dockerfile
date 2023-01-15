FROM python:3.11-slim

ARG DJANGO_MEDIA_ROOT

ENV DJANGO_MEDIA_ROOT ${DJANGO_MEDIA_ROOT}

ENV PYTHONUNBUFFERED 1  
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE="apigram.settings.docker"


RUN apt-get update \  
  && apt-get install -y --no-install-recommends git build-essential libpq-dev curl \  
  && rm -rf /var/lib/apt/lists/*

RUN pip install uwsgi

COPY requirements.txt /tmp/requirements.txt

RUN pip install --cache-dir /tmp/cache -r /tmp/requirements.txt \  
    && rm -rf /tmp/requirements.txt

WORKDIR /app

COPY apigram/ .
COPY assets/default.jpg $DJANGO_MEDIA_ROOT/account_photos/
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

RUN chmod a+x /app/docker-entrypoint.sh


ENTRYPOINT ["/app/docker-entrypoint.sh"]
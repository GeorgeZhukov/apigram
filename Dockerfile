FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1  
ENV PYTHONDONTWRITEBYTECODE 1
ENV DJANGO_SETTINGS_MODULE="apigram.settings.docker"


RUN apt-get update \  
  && apt-get install -y --no-install-recommends build-essential libpq-dev \  
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt

RUN pip install --cache-dir /tmp/cache -r /tmp/requirements.txt \  
    && rm -rf /tmp/requirements.txt

WORKDIR /app

COPY apigram/ .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000

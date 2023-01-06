FROM python:3.11
ENV DJANGO_SETTINGS_MODULE="apigram.settings.docker"
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY apigram/ .

RUN python manage.py collectstatic --no-input

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000

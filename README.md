# apigram
Simple REST Api application written on django and djangorestframework. Provides a simple api for uploading and displaying photos


## Installation

Before installation, check this config: `apigram/apigram/settings.py`
Specially `DATABASES` section.

It is assumed that you are running a postgresql server.


```bash

virtualenv venv && source venv/bin/activate
pip install -r requirements.txt

cd apigram/
cp .env.example .env # Change this key if you'll deploy production

./manage.py migrate
./manage.py runserver
```


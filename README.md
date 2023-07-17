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



### Renew SSL certificate

```bash
pip install certbot certbot-nginx
certbot certonly --manual
```

Update nginx config, add location aka `/.well-known/acme-challenge/` from certbot with given token
Restart docker containers



### Example Nginx config

```nginx
upstream django {
    # server unix:///path/to/your/mysite/mysite.sock; # for a file socket
    server app:8000; # for a web port socket (we'll use this first)
}
#server {
#    listen 8001 ;
#    server_name localhost;
#    location /.well-known/acme-challenge/bgsqvj1AiC0EGZ-0JV9-invHcJ7NXnZDfLPdrAesUS8{
#        return 200 'bgsqvj1AiC0EGZ-0JV9-invHcJ7NXnZDfLPdrAesUS8.HMScfy4c3p_vTsGIDtF_8a1v-ewVI37KrpE_9NPOCrU';
#    }
#}

server {
    listen 8001 default_server;

    server_name _;

    return 301 https://$host$request_uri;
}

# configuration of the server
server {
    # the port your site will be served on
    listen 8000 ssl;
    server_name 35.228.191.56 apigram.crabdance.com localhost;

    ssl_certificate     /etc/nginx/templates/cert.pem;
    ssl_certificate_key /etc/nginx/templates/key.pem;

    # the domain name it will serve for
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /usr/src/app/apigram/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /usr/src/app/apigram/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /etc/nginx/uwsgi_params; # the uwsgi_params file you installed
    }
}
```



### Deploy with docker

```bash
docker compose -f docker-compose.yml -f docker-compose.production.yml up -d
```
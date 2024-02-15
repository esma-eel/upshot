# How To ?

## Set project folder in virtualenvwrapper
to cd to project folder when using "workon envname" command
enter "setvirtualenvproject" in root

to add project to python path and use django-admin insteado f python manage.py
use add2virtualenv . 
note: "." is current folder of project

## Setup environment variables
if you use virtualenv else use only export command in global
or put the export command in .bashrc or .zshrc files

cd ~/.virtualenvs/$NAMEOFVENV/bin
vim postactivate
    export DJANGO_SETTINGS_MODULE=config.settings.local
    export SECRET_KEY=""
    export CELERY_BROKER_URL=""

vim postdeactivate
    unset DJANGO_SETTINGS_MODULE
    unset SECRET_KEY
    unset CELERY_BROKER_URL

## Run commands of management.py
if you set previous step
you only need to set settings in postactivate and unset it in postdeactivate
but if you did not want to use env variables use below command

python manage.py cmdname --settings=config.settings.local


## Create app
mkdir ./upshot/appname
django-admin startapp appname ./upshot/appname

add codes below to apps.py

    name = "upshot.appname"
    verbose_name = _("Appname")

    def ready(self):
        pass

## flusth expired tokens
python manage.py flushexpiredtokens


## run redis server
docker compose -f dc-redis.yml up -d --build

## connect to a container
to go with root in a container
docker exec -it -u 0 redis_server sh 

to go with noraml user in a container
docker exec -it -u 1 redis_server sh

## celery 
./doker/celery/celery.Runner.sh
i did some works on celery but finally i had to run the sh above
to use it in localhost

## adminstration
create models in models/ module
with name of that category then import it
in the __init__.py of models/ module

### sms templates
create sms template of otp from admin first
create otp1 template
in sms service provider
with token variable

example
name:
    otp1
template text:
    Test
    Code: %token
### api key
create api key of sms provider in admin first
code for sms provider is 
"sms_provider_key"

## Email SMTP testing
to see sent emails for testing you have to run mailpit server with docker
docker compose -f doker/mailpit/dc-mailpit.yml up -d --build

settings to work are
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = 1025
then use send mail function
from django.core.mail import send_mail

### email templates
create email template of otp from admin first
create otp1 template
add token
example
name:
    otp1
template text:
    Test
    Code: {token}

name:
    otl1
template text:
    Link of password reset:
    Link: {link}

    Important: Link is active for 6 hours


## start commands for local
docker compose -f doker/redis/dc-redis.yml up -d --build
docker compose -f doker/mailpit/dc-mailpit.yml up -d --build
./doker/celery/celery.Runner.sh 

### down services
./doker/celery/celery.Runner.sh --> ctrl + c
docker compose -f doker/mailpit/dc-mailpit.yml down
docker compose -f doker/redis/dc-redis.yml down

## run all tests
to run tests you can refert to the module or use command below to run all
python manage.py test -v 2 upshot

# TODO:
- remember to use .env files for docker later
- later you should put execution files of celery run in docker-compose (just a reminder)

# Update:
- project is dockerized now
- you can run project with local.yml and production.yml based on desiered env
- on a new system you have to copy envs_template to .envs and change files
    in order to work

- mailpit is for local dev
- staging.yml and test.yml has no data are just placeholders
- sms does not work unless you change project to use other services
  or add your api key of kavenegar in api keys part

# todo:
- add letsencrypt or use ssl files you bought based on project



# OLD readme
# comprehensive system of student papers and exchange space between software industry professionals
My final project of university is 
A comprehensive system of student papers and exchange space between software industry professionals
which give users a space to publish their articles or be mentor of other students or send a mentor request to some one.

My Professor: Mr.Amir Marooy


## Getting Started

download the project and then  
create your virtual env like this  
virtualenv venv  
then  
pip install -r /path/to/requirements.txt

### Prerequisites

you should have

```
Django==2.2.3
django-fs-trumbowyg==0.1.4
Pillow==6.1.0
psycopg2==2.8.3
pytz==2019.1
sqlparse==0.3.0

```
note: other requirements will be added as soon as the project finished
## Deployment

for deploy a django project you can use  
* [DigitalOceanGuide](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-local-django-app-to-a-vps) - Digital Ocean's Guide

## Built With

* [Django](https://www.djangoproject.com/) - The python web framework used
* [Python](https://www.python.org/) - The programming language used
* [BootStrap](https://getbootstrap.com/) - The css framework used

## Authors

* **Esmaeel Komijani** - *Initial work* - [EsmaeelKomijani](http://esmaeelkomijani.ir)

## Special Thanks To
* **Mr.Amir Marooy** = *Professor* - [Mr.AmirMarooy](http://amirmarooy.ir/)

## Notes

* Nothing Yet
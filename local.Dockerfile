###########
# BUILDER #
###########

# pull official base image
FROM python:3.11.7 as builder

# set work dir
WORKDIR /usr/src/app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint and format
RUN pip install --upgrade pip
# RUN pip install black==23.12.1
# RUN pip install flake8==7.0.0
COPY . /usr/src/app/
# RUN flake8 --ignore=E501,F401 .
# RUN black --line-length 80 --experimental-string-processing .

# install dependencies
COPY ./requirements/base.txt base.txt
# note: change this based on your environment
COPY ./requirements/production.txt requirements.txt
# *1. if you dont want to have cache in docker in order to decrease image size, else comment code below
# RUN pip wheel --timeout 60 --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.11.7 as final

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/_static_root
RUN mkdir $APP_HOME/_media
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat-traditional libpq-dev 
# if you uncommented *.1 else comment line below and uncomment base.txt line
# COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/base.txt .
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --timeout 60 --upgrade pip
# if you dont want to have cache and you removed comment of *.1 above use below command else -
# RUN pip install --timeout 60 --no-cache /wheels/*
# - uncomment this line
RUN pip install --timeout 60 -r requirements.txt

# copy entrypoint
COPY ./entrypoint.production.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.production.sh
RUN chmod +x $APP_HOME/entrypoint.production.sh

# copy django commands
COPY ./dj.commands.production.sh .
RUN sed -i 's/\r$//g' $APP_HOME/dj.commands.production.sh
RUN chmod +x $APP_HOME/dj.commands.production.sh


# copy celery commands
COPY ./celery.runner.production.sh .
RUN sed -i 's/\r$//g' $APP_HOME/celery.runner.production.sh
RUN chmod +x $APP_HOME/celery.runner.production.sh


# copy env file --> change this based on environment
COPY ./config/.envs/django/.env.local.django ./config/.envs/.env.default

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint
ENTRYPOINT ["/home/app/web/entrypoint.production.sh"]
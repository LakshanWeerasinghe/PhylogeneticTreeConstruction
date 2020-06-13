# pull official base image
FROM python:3.7-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apt-get update \  
    && apt-get -y upgrade \
    && apt-get install -y apt-utils \
    && apt-get install -y python3-pip 

RUN apt-get install -y libpq-dev postgresql postgresql-contrib \
    && pip3 install -U setuptools 

RUN apt-get install -y make automake gcc g++ subversion python3-dev musl-dev

# install cmake
RUN apt-get install -y cmake\
    && rm -rf /var/lib/apt/lists/*


# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip3 install -r requirements.txt


# copy project
COPY . .

RUN chmod +x ./entrypoint.sh
RUN chmod -R 777 ./dsk


# # add and run as non-root user
# RUN adduser -D myuser
# USER myuser


CMD ["sh", "entrypoint.sh" ]
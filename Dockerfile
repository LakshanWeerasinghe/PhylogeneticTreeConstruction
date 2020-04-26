# # pull official base image
# FROM python:3.7-alpine3.10

# # set work directory
# WORKDIR /usr/src/app

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # install psycopg2
# RUN apk update \
#     && apk add --virtual build-deps gcc python3-dev musl-dev \
#     && apk add postgresql-dev \
#     && pip install psycopg2 \
#     && apk del build-deps \
#     && apk add bash 

# RUN apk add make automake gcc g++ subversion python3-dev 

# # install cmake
# RUN apk add cmake

# # install dependencies
# COPY ./requirements.txt /usr/src/app/requirements.txt
# RUN pip install -r requirements.txt


# # copy project
# COPY . .

# RUN chmod +x ./entrypoint.sh
# RUN chmod -R 777 ./dsk


# # # add and run as non-root user
# # RUN adduser -D myuser
# USER root


# CMD ["sh", "entrypoint.sh" ]


# pull official base image
FROM python:3.7-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apt update \  
    && apt install -y gcc python3-dev musl-dev \
    && apt install -y postgres-server-dev-all \
    && pip install -y psycopg2 \
    && apt install -y  bash 

RUN apt install make automake gcc g++ subversion python3-dev 

# install cmake
RUN apt install cmake\
    && rm -rf /var/lib/apt/lists/*


# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt


# copy project
COPY . .

RUN chmod +x ./entrypoint.sh
RUN chmod -R 777 ./dsk


# # add and run as non-root user
# RUN adduser -D myuser
# USER myuser


CMD ["sh", "entrypoint.sh" ]


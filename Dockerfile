# pull official base image
FROM python:3.7-alpine3.10

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps 

RUN apk add make automake gcc g++ subversion python3-dev 

# install cmake
RUN apk add cmake

# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN chmod +x ./entrypoint.sh

# # add and run as non-root user
# RUN adduser -D myuser
# USER myuser

CMD ["sh", "entrypoint.sh" ]

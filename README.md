## Installation

1. `pip install -r requirements.txt`
2. `python manage.py makemigations`
3. `python manage.py migrate`
4. `python manage.py createsuperuser --email admin@example.com --username admin`
5. `python manage.py runserver` 

## Postgresql installation

```bash

sudo apt-get update
sudo apt-install python-pip python-dev libpq-dev postgresql postgresql-contrib

sudo su - postgres
psql
```
In the postgres console 

```sql
CREATE DATABASE dna_tree;
CREATE USER lakshan WITH PASSWORD 'lakshan';
ALTER ROLE lakshan SET client_encoding TO 'utf8';
ALTER ROLE lakshan SET default_transaction_isolation TO 'read committed';
ALTER ROLE lakshan SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE dna_tree TO lakshan;
\q
```


# Docker

There are two docker compose files within this repository:

* ``docker-compose.yml`` contains the dev environment
* ``prod.yml`` contains the production environment

# Dev Environment

sudo docker-compose exec db psql -U postgres

sudo docker-compose exec db psql -U lakshan -W dna_tree

Setting up the docker dev environment is quite simple (it is assumed you have docker up and running, and you know how to use docker-compose):

1. Run ```docker-compose build``` to build the Dockerfiles for this project
2. Run migrations: ```docker-compose run --rm python python manage.py migrate```
3. Create a super user: ```docker-compose run --rm python python manage.py createsuperuser```
4. Last but not least, we can start all services using ```docker-compose up```. You should be able to access the app via **http://0.0.0.0:8000/** in your browser.
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

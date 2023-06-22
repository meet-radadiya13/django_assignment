# Django Assignment

#### 1. Clone this repository:
* `git clone https://github.com/meet-radadiya13/django_assignment.git`
#### 2. Create virtual environment:
* `sudo apt install virtualenv`
* `virtualenv --python='/usr/bin/python3.6' venv`
* `source venv/bin/activate`
* `cd django_assignment/`
#### 3. Install dependencies:
* `pip install -r requirements.txt`
#### 4. Install postgresql
* `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`
* `sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'`
* `sudo apt update`
* `sudo apt-get install postgresql-10`
#### 5. Create database
* `sudo su - postgres`
* `postgres@xxx:~$ psql`
  * `create database <db_name>;`
  * `create user <admin_name> password ;`
  * `grant all privileges on database <db_name> to <admin_name>;`
  * `postgres=# \q`
  * `postgres@xxx:~$ exit`
#### 6. Create local.py in django_assignment/
* local.py content:
```python
DEBUG = True
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': '<django_project>',
    'USER': '<admin_name>',
    'PASSWORD': '<password>',
    'HOST': 'localhost',
    'PORT': '5432',
  }
}
SECRET_KEY = '<secret_key>'

EMAIL_HOST_USER = '<email_id>'
EMAIL_HOST_PASSWORD = '<password>'

STRIPE_PUBLIC_KEY = '<pubic_key>'
STRIPE_SECRET_KEY = '<secret_key>'
```
#### 7. Run migrations:
```
python3 manage.py migrate
```
#### 8. Create superuser:
```
python3 manage.py createsuperuser
```
#### 9. Run the server:
```
python3 manage.py runserver
```
#### 10. Browse below url:
* Admin url: - http://localhost:8000/project_admin/

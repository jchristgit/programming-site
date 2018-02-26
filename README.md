# Programming Discord Website
This repository contains our website, which is used for
many different functions such as showing server statistics,
allowing the reading and writing of programming guides, and more.


### Setup
If you don't have it already, [install `pipenv`](https://docs.pipenv.org/#install-pipenv-today).
To install the dependencies for the project, use `pipenv install`.

Once that's done, you need to configure the Django
project itself. First, run `pipenv run python manage.py migrate`
to apply all migrations to the database (this is a 
SQLite database for development). Next, create a
superuser using `pipenv run python manage.py createsuperuser`.

To set OAuth integration with Discord up, follow
the [post-installation instructions for `django-allauth`](https://django-allauth.readthedocs.io/en/latest/installation.html#post-installation). 

Finally, to start the app, simply use `pipenv run python manage.py runserver`.

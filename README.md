# Programming Discord Website
This repository contains our website, which is used for
many different functions such as showing server statistics,
allowing the reading and writing of programming guides, and more.


## Initial Setup
*The commands used here assume you're running from within the virtual
environment, excluding the pipenv installation step. You can run them
using either `pipenv run 'command'` or within `pipenv shell`.*


If you don't have it already, [install `pipenv`](https://docs.pipenv.org/#install-pipenv-today).
To install the dependencies for the project, use `pipenv install`.

Once that's done, you need to configure the Django
project itself. First, run `python manage.py migrate`
to apply all migrations to the database (this is a 
SQLite database for development). Next, create a
superuser using `python manage.py createsuperuser`.

To set OAuth integration with Discord up, follow
the [post-installation instructions for `django-allauth`](https://django-allauth.readthedocs.io/en/latest/installation.html#post-installation).
Basically, you need to change the site domain of the one site
within the database (it defaults to `example.com`, put whatever you use
to access your local site there, probably `127.0.0.1:8000`),
add a social application linked to the site, and you should be set.
**Make sure that you use `discoauth` instead of `discord` for the social application.**
Do note that you will have to set your redirect URL
to `http://127.0.0.1:8000/accounts/discoauth/login/callback/`, otherwise it won't work.

Next up, you need to set up your environment variables.
We recommend putting these into a file called `.env`,
since `pipenv` loads variables contained there automatically.
The following are required:
- `PGSQL_URL` (in the form `postgres://user:pass@host/dbname`)
- `DISCORD_GUILD_ID`

These should be fairly self-explanatory, but keep in mind that
you need to point the `PGSQL_*` settings to a database used by
an instance of [statbot](https://github.com/strinking/statbot).
You can view setup instructions for statbot on the linked repository,
a `docker-compose.yml` file is included for simple setup.
If your PostgreSQL instance does not support SSL, set the
environment variable `PGSQL_NO_SSL` to any truthy value.

Setting `DISCORD_WEBHOOK_URL` is optional.

Now that you've went through the long and motivating process of setting
it up, you're finally able to run it locally...

## Local Development
Finally, to start the app, simply use `python manage.py runserver`.
Set the environment variable `DEBUG` to `1` to enable debug mode,
for example with `DEBUG=1 python manage.py runserver`.

Running tests is sadly a bit more complicated, but it's also a one-time setup.
You need to have the environment variables 
- `PGSQL_TEST_URL` (in the form `postgres://user:pass@host/dbname`)

set, which should be self-explanatory. Do *not* point these to the
same values that you were using above. Bad idea.

Finally, to run the tests, simply use `python manage.py test`.
You can also use the `--keepdb` flag which may speed them up a fair bit.

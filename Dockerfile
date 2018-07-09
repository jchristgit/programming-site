FROM kennethreitz/pipenv

COPY . /site
WORKDIR /site

RUN pipenv clean
RUN pipenv sync

EXPOSE 80

CMD ["pipenv", "run", "python", "manage.py", "runserver"]

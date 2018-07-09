FROM kennethreitz/pipenv

ENV PYTHONUNBUFFERED 1

COPY . /app

CMD ["python3", "manage.py", "runserver"]

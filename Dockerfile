FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1

# Set working directory
WORKDIR /code

# copy pipfiles
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

# copy project to working directory
COPY . /code/

CMD gunicorn config.wsgi -b 0.0.0.0:$PORT
FROM python:3.8.5

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip \
    && pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --ignore-pipfile --deploy

COPY cogs/ custom/ main.py ./

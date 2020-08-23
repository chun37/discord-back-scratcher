FROM python:3.8.5

WORKDIR /usr/src/app

RUN pip install --upgrade pip \
    && pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --ignore-pipfile --deploy

COPY src/ ./src/

CMD ["python", "src/main.py"]
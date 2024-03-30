FROM python:3.10-slim-buster

WORKDIR /app

ADD Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --system --deploy

ADD . /app

EXPOSE 8000

CMD ["arkive-web-service"]
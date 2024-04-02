FROM python:3.10-slim-buster

WORKDIR /app

ADD Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

ADD ./src /app/src

ADD .env /app/.env

EXPOSE 8000

ENV PYTHONPATH=src

# RUN chmod +x ./bin/docker-entrypoint.sh

# CMD ["./bin/docker-entrypoint.sh"]

CMD python -m uvicorn arkive_web_service.__main__:app --host 0.0.0.0 --port 8000
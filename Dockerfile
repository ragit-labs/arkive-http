FROM python:3.10-slim-buster

WORKDIR /app

ADD Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

ADD . /app

EXPOSE 8000

ENV PYTHONPATH=src
ENV OPENAI_API_KEY="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"

# RUN chmod +x ./bin/docker-entrypoint.sh

# CMD ["./bin/docker-entrypoint.sh"]

# CMD ["ls", "src"]

CMD ["uvicorn", "arkive_web_service.__main__:app", "--host", "0.0.0.0", "--port", "8000"]
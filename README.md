# FastAPI/Celery/Docker example

Basic setup for a `FastAPI` application distributing work
to workers via `celery`.

Written as a `python` package built in `docker` containers
and orchestrated with `docker compose`.

## refs

+ `Celery`
    + main page: https://docs.celeryproject.org
    + configuration: https://docs.celeryproject.org/en/stable/userguide/configuration.html#configuration
    + brokers and backends: https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/

    + RabbitMQ configuration: https://www.rabbitmq.com/configure.html

+ `FastAPI`
    + https://fastapi.tiangolo.com/

## usage

```bash
docker-compose up --build

curl http://localhost:8000/
curl -X POST http://localhost:8000/slow-worker
curl -X POST http://localhost:8000/fast-worker
curl http://localhost:8000/slow-worker
```

# Deployment options

This example deploys with `RabbitMQ` as a broker and `redis` as a backend.
There are many other options (see: https://docs.celeryproject.org/en/stable/userguide/configuration.html)

For example, an AWS deployment could use `AWS SQS` as the broker and `AWS DynamoDB` as the backend,
with the containers hosted in `AWS Fargate`.

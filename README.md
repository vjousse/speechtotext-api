# Speech to text - API

This project provides a simple HTTP API as a frontend to any Sppech Recognition service like [Kaldi](https://kaldi-asr.org). It's even more generic: it provides a simple interface to any script taking a file as input and sending multiple files as results.

It's written in Python using [FastAPI](https://fastapi.tiangolo.com/) for the web framework, [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/) for the async ORM and [dramatiq](https://dramatiq.io/) for managing the background tasks. The stack is using Nginx, Redis and PostgreSQL. And of course, everything is available using Docker images.

## Docker

### Web application

    docker-compose --env-file .env.docker up

### Kaldi worker

    docker-compose -f docker-compose-worker.yml --env-file .env.docker up --build

## Install

    pip install -r requirements.txt

## Run

Web API:

    uvicorn app.main:app --reload --reload-dir app

Task manager (dramatiq):

    dramatiq asr_worker.download

## Configure

Configuration can be found in `app/core/config.py`.

## Init database

    aerich init-db

## Testing

    pytest --disable-warnings -s app/tests

The `-s` flag is used to show captured stdout (print) even if the test is successful.

## Files

Upload a file:


        curl -L -v \
            -F file=@/home/vjousse/wifi.md \
            -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiODAwZTk1NjQtNjgwNC00YWI1LWJjNTktYTA4ODE4MjIyN2JlIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE2MzA1MDU5ODN9.W6eq5DZMteTSHMZ1bxlqGaBsQTyqpCSYPSTdJcK3C04" \
            http://localhost:8000/api/file/upload

## Users

Using [FastAPIUsers](https://fastapi-users.github.io/fastapi-users/usage/flow/)

### Registering

    curl \
        -H "Content-Type: application/json" \
        -X POST \
        -d "{\"email\": \"phil@phil.com\",\"password\": \"phil\"}" \
        http://localhost:8000/auth/register

or

    http POST http://localhost:8000/auth/register email=phil@phil.com password=phil --session=session

Returns:

```json
{
    "id":"800e9564-6804-4ab5-bc59-a088182227be",
    "email":"phil@phil.com",
    "is_active":true,
    "is_superuser":false,
    "is_verified":false
}
```

### Login

    curl \
        -H "Content-Type: multipart/form-data" \
        -X POST \
        -F "username=phil@phil.com" \
        -F "password=phil" \
        http://localhost:8000/auth/jwt/login

Returns:

```json
{
    "access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiODAwZTk1NjQtNjgwNC00YWI1LWJjNTktYTA4ODE4MjIyN2JlIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE2MzAxMzk5OTJ9.w-ZWpm51fyybFivmKjun3qbXuqwXCgYyxGbPD1yhIr4",
    "token_type":"bearer"
}
```

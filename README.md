# URL SHORTNER API

This API was made to shorten urls.

## Requirements:
- The short url must be unique
- When a short url is accessed the application will redirect you to the long url
- You can choose a customized short url
- All short urls have a expiration date and time
    - You can set your expiration date and time manually
    - The default expiration time is 5 days
- Short urls are not being generated using the long url, so it is random and not predictable
- This application is using a NoSQL database

## Tech Stack
- Python - Programming Language
- FastAPI - REST API
- Mongo - Database
- MongoEngine - ORM
- Docker - Containerization

## Application urls:

- OpenApi documentation: http://localhost:8080/redoc
- Swagger documentation: http://localhost:8080/docs

## How to run it
For both scenarios you must have a `.env` file with your database information looking like this:

```
MONGO_INITDB_ROOT_USERNAME=yourdatabaseuser
MONGO_INITDB_ROOT_PASSWORD=yourdatabasepass
MONGO_INITDB_DATABASE=yourdatabasename
```

If you run the database locally with the docker this file will provide the information to create your database.

### **Local environment with Pipenv**
Make sure you have installed:
- Python at least 3.10
- Pipenv
- Docker

Run the API:

    pipenv shell
    pipenv install
    docker-compose up mongodb
    uvicorn main:app

Run tests:

    python -m unittest

### **Local environment with docker**
Make sure you have installed:
- Docker

Run the API:

    docker-compose up app

Run the tests:

    docker-compose up test
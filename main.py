import os

from fastapi import FastAPI
from mongoengine import connect
from dotenv import load_dotenv

from src.views import router

load_dotenv()

app = FastAPI(
    title='URL Shortener',
    description='This API was made to make your urls tiny'
)

MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_DB = os.getenv('MONGO_INITDB_DATABASE')
MONGO_HOST = os.getenv('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.getenv('MONGO_PORT', '27017'))

connect(
    db=MONGO_DB,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    host=MONGO_HOST,
    port=MONGO_PORT
)

app.include_router(router)

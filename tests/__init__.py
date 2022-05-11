import unittest

from mongoengine import connect, disconnect
from fastapi.testclient import TestClient

from main import app


class TestBase(unittest.TestCase):
    client = TestClient(app)

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

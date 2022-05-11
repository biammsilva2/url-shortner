from datetime import datetime, timedelta

from mongoengine.errors import NotUniqueError

from src.models import ShortUrl
from . import TestBase


class TestModel(TestBase):

    def test_short_url_unique(self):
        url_object = ShortUrl(
            short_url='short_link_test', long_url='http://localhost:8000'
        )
        url_object.save()

        assert url_object.short_url == 'short_link_test'

        url_object1 = ShortUrl(
            short_url='short_link_test', long_url='http://localhost:8000'
        )

        with self.assertRaises(NotUniqueError):
            url_object1.save()

    def test_url_not_longer_available(self):
        url_object = ShortUrl(
            short_url='test',
            long_url='http://localhost:8001',
            timespan=datetime.now()
        )
        url_object.save()
        assert not url_object.validate_link()

    def test_url_available(self):
        url_object = ShortUrl(
            short_url='test1',
            long_url='http://localhost:8002',
            timespan=datetime.now() + timedelta(days=5)
        )
        url_object.save()
        assert url_object.validate_link()

from . import TestBase
from src.models import ShortUrl
from src.services import ShortenUrlService


class TestService(TestBase):

    def test_is_short_url_not_in_database(self):
        assert not ShortenUrlService.is_short_url_on_database('123456')

    def test_is_short_url_in_database(self):
        ShortUrl(
            short_url='abc124',
            long_url='https://github.com/tiangolo/fastapi/issues/790'
        ).save()
        assert ShortenUrlService.is_short_url_on_database('abc124')

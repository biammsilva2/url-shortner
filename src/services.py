import uuid

from src.models import ShortUrl


class ShortenUrlService:

    @classmethod
    def shorten_random_url(cls, host: str) -> str:
        short_url = cls.generate_short_url(host)
        while ShortenUrlService.is_short_url_on_database(short_url):
            short_url = cls.generate_short_url(host)
        return short_url

    @staticmethod
    def generate_short_url(host: str) -> str:
        return host + str(uuid.uuid4())[-6:]

    @staticmethod
    def is_short_url_on_database(short_url: str) -> bool:
        return len(ShortUrl.objects(short_url=short_url)) > 0

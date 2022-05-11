import uuid

from src.models import ShortUrl


class ShortenUrlService:

    @classmethod
    def shorten_random_url(cls) -> str:
        short_url = cls.generate_short_url()
        while ShortenUrlService.is_short_url_on_database(short_url):
            # TODO: change to use the collection id
            short_url = cls.generate_short_url()
        return short_url

    @staticmethod
    def generate_short_url() -> str:
        return str(uuid.uuid4())[-6:]

    @staticmethod
    def is_short_url_on_database(short_url: str) -> bool:
        # TODO: Implement with mongoengine exception
        return len(ShortUrl.objects(short_url=short_url)) > 0

import uuid
from fastapi import HTTPException

from mongoengine.errors import DoesNotExist, MultipleObjectsReturned

from src.models import ShortUrl


class ShortenUrlService:

    @classmethod
    def shorten_random_url(cls) -> str:
        short_url = cls.generate_short_url()
        counter = 1
        while ShortenUrlService.is_short_url_on_database(short_url):
            short_url = cls.generate_short_url()
            counter += 1
            if counter >= 100:
                raise HTTPException(
                    status_code=422,
                    detail='No url available at the moment, try again later'
                )
        return short_url

    @staticmethod
    def generate_short_url() -> str:
        return str(uuid.uuid4())[-6:]

    @staticmethod
    def is_short_url_on_database(short_url: str) -> bool:
        try:
            return ShortUrl.objects(short_url=short_url).get()
        except DoesNotExist:
            return False
        except MultipleObjectsReturned:
            return False

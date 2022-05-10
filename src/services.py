import uuid


class ShortenUrlService:

    @staticmethod
    def shorten_random_url(host: str) -> str:
        return host + str(uuid.uuid4())[-6:]

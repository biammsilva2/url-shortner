from mongoengine import Document, URLField


class ShortUrl(Document):
    long_url = URLField(required=True)
    short_url = URLField(required=True)

    def parse_object(self) -> dict:
        return {
            'id': str(self.pk),
            'long_url': self.long_url,
            'short_url': self.short_url
        }

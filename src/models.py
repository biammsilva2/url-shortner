from mongoengine import Document, URLField, StringField


class ShortUrl(Document):
    long_url = URLField(required=True, primary_key=True)
    short_url = StringField(required=True)

    def parse_object(self, host: str) -> dict:
        return {
            'long_url': self.long_url,
            'short_url': host + self.short_url
        }

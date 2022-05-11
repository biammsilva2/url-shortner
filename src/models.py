import datetime

from mongoengine import Document, URLField, StringField, DateTimeField
from mongoengine import BooleanField, IntField


class ActiveShortUrlWrapper(object):
    def __get__(self, instance, owner):
        return ShortUrl.objects.filter(is_active=True)


class ActiveShortUrl:
    objects = ActiveShortUrlWrapper()


class ShortUrl(Document):
    long_url = URLField(required=True)
    short_url = StringField(required=True, unique=True)
    is_active = BooleanField(default=True)
    timespan = DateTimeField(
        default=datetime.datetime.now() + datetime.timedelta(days=5)
    )
    redirects_count = IntField(default=0)

    def validate_link(self):
        if self.is_active:
            if self.timespan <= datetime.datetime.now():
                self.is_active = False
                return False
        return True

    def parse_object(self, host: str = '') -> dict:
        return {
            'long_url': self.long_url,
            'short_url': host + self.short_url,
            'is_active': self.is_active,
            'timespan': str(self.timespan),
            'redirects_count': self.redirects_count
        }

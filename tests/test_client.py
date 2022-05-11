from datetime import datetime, timedelta
from src.models import ShortUrl
from . import TestBase


class TestCreateShortClient(TestBase):

    def test_create_new_short_url(self):
        response = self.client.post(
            "/shorten",
            json={
                "url": "https://fastapi.tiangolo.com/tutorial/testing/"
            },
        )
        assert response.status_code == 201

    def test_create_new_short_url_custom_short_url(self):
        response = self.client.post(
            "/shorten",
            json={
                "url": "https://fastapi.tiangolo.com/",
                "custom_short_link": "test"
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            'long_url': "https://fastapi.tiangolo.com/",
            'short_url': 'http://testserver/test'
        }

    def test_create_short_url_long_url_exists(self):
        ShortUrl(
            short_url='short_link',
            long_url='https://fastapi.tiangolo.com/tutorial/'
        ).save()
        response = self.client.post(
            "/shorten",
            json={
                "url": "https://fastapi.tiangolo.com/tutorial/",
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            'long_url': "https://fastapi.tiangolo.com/tutorial/",
            'short_url': 'http://testserver/short_link'
        }

    def test_create_short_url_short_url_exists(self):
        ShortUrl(
            short_url='test3',
            long_url='http://localhost:8003'
        ).save()
        response = self.client.post(
            "/shorten",
            json={
                "url": "http://localhost:8030",
                "custom_short_link": 'test3'
            },
        )
        assert response.status_code == 409
        assert response.json() == {'detail': "short url already exists"}

    def test_create_short_url_with_timespan(self):
        response = self.client.post(
            "/shorten",
            json={
                "url": "http://localhost:8004",
                "custom_short_link": 'test4',
                'timespan': str(datetime.now() + timedelta(days=5))
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "long_url": "http://localhost:8004",
            "short_url": 'http://testserver/test4',
        }


class TestAccessShortClient(TestBase):

    def test_get_short_url(self):
        ShortUrl(
            short_url='abc123',
            long_url='https://fastapi.tiangolo.com/tutorial/request-forms/'
        ).save()
        response = self.client.get('/abc123', allow_redirects=False)
        assert response.status_code == 303

    def test_get_short_url_does_not_exist(self):
        response = self.client.get('/123456', allow_redirects=False)
        assert response.status_code == 404
        assert response.json() == {"detail": "Short Url not found"}

    def test_get_short_url_timespan_expired(self):
        ShortUrl(
            short_url='test2',
            long_url='http://localhost:8002',
            timespan=datetime.now()
        ).save()
        response = self.client.get('/test2', allow_redirects=False)
        assert response.status_code == 422
        assert response.json() == {"detail": "Link no longer available"}


class TestShortAnalyticsClient(TestBase):

    def test_get_short_url(self):
        ShortUrl(
            short_url='test5',
            long_url='http://localhost:8005',
            timespan=datetime(2022, 5, 16, 20, 25, 0)
        ).save()
        response = self.client.get('/analytics/test5')
        assert response.status_code == 200
        assert response.json() == {
            'long_url': 'http://localhost:8005',
            'short_url': 'test5',
            'redirects_count': 0,
            'timespan': '2022-05-16T20:25:00',
            'is_active': True
        }

    def test_get_short_url_does_not_exist(self):
        response = self.client.get('/analytics/123456', allow_redirects=False)
        assert response.status_code == 404
        assert response.json() == {"detail": "Short Url not found"}

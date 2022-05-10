from fastapi import APIRouter, Request

from src.models import ShortUrl
from src.schemas import ShortnerUrlSchema, ShortnerUrlInputSchema
from src.services import ShortenUrlService


router = APIRouter()


@router.post('/shorten', response_model=ShortnerUrlSchema)
def shorten_url_endpoint(item: ShortnerUrlInputSchema, request: Request):
    short_url = ShortenUrlService.shorten_random_url(str(request.base_url))
    short_url_object = ShortUrl(short_url=short_url, long_url=item.url).save()
    return short_url_object.parse_object()

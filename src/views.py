from fastapi import APIRouter, Request

from src.schemas import ShortnerUrlSchema, ShortnerUrlInputSchema
from services import ShortenUrlService


router = APIRouter()


@router.post('/shorten', response_model=ShortnerUrlSchema)
def shorten_url_endpoint(item: ShortnerUrlInputSchema, request: Request):
    short_url = ShortenUrlService.shorten_random_url(str(request.base_url))
    return {
        'id': 1,
        'long_url': item.url,
        'short_url': short_url
    }

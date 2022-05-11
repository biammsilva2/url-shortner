from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from mongoengine.errors import DoesNotExist

from src.models import ActiveShortUrl, ShortUrl
from src.schemas import ShortnerUrlSchema, ShortnerUrlInputSchema
from src.services import ShortenUrlService


router = APIRouter()


@router.post('/shorten', response_model=ShortnerUrlSchema)
def shorten_url_endpoint(item: ShortnerUrlInputSchema, request: Request):
    if (short_url := item.custom_short_link):
        if ShortenUrlService.is_short_url_on_database(short_url):
            raise HTTPException(409, detail="short url already exists")
    else:
        if (short_url_object := ActiveShortUrl.objects(
            long_url=item.url
        ).first()):
            return short_url_object.parse_object(host=str(request.base_url))
        short_url = ShortenUrlService.shorten_random_url()
    short_url_data = {
        'short_url': short_url,
        'long_url': item.url
    }
    if item.timespan:
        short_url_data['timespan'] = item.timespan
    short_url_object = ShortUrl(**short_url_data).save()
    return short_url_object.parse_object(host=str(request.base_url))


@router.get('/{short_url_token}')
def redirect_to_long_url(short_url_token: str):
    try:
        short_url_object = ActiveShortUrl.objects(
            short_url=short_url_token
        ).get()
        short_url_object.validate_link()
    except DoesNotExist:
        raise HTTPException(404, detail="Short Url not found")
    return RedirectResponse(url=short_url_object.long_url, status_code=303)


@router.get('/analytics/{short_url_token}', response_model=ShortnerUrlSchema)
def analytics(short_url_token: str):
    try:
        short_url_object = ActiveShortUrl.objects(
            short_url=short_url_token
        ).get()
        short_url_object.validate_link()
    except DoesNotExist:
        raise HTTPException(404, detail="Short Url not found")
    return short_url_object.parse_object()

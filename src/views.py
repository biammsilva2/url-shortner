from fastapi import APIRouter, Request, HTTPException, status, Response
from fastapi.responses import RedirectResponse
from mongoengine.errors import DoesNotExist, NotUniqueError

from src.models import ActiveShortUrl, ShortUrl
from src.schemas import (
    ShortnerUrlSchema,
    ShortnerUrlInputSchema,
    ShortnerUrlAnalyticsSchema,
)
from src.services import ShortenUrlService


router = APIRouter()


@router.post('/shorten', response_model=ShortnerUrlSchema)
def shorten_url_endpoint(item: ShortnerUrlInputSchema, request: Request,
                         response: Response):

    if (short_url_object := ActiveShortUrl.objects(long_url=item.url).first()):
        response.status_code = status.HTTP_200_OK
    else:
        short_url = item.custom_short_link or \
                    ShortenUrlService.shorten_random_url()
        short_url_data = {
            'short_url': short_url,
            'long_url': item.url
        }
        if item.timespan:
            short_url_data['timespan'] = item.timespan
        try:
            short_url_object = ShortUrl(**short_url_data).save()
        except NotUniqueError:
            raise HTTPException(409, detail="short url already exists")
        response.status_code = status.HTTP_201_CREATED

    return short_url_object.parse_object(host=str(request.base_url))


@router.get('/{short_url_token}', response_class=RedirectResponse,
            status_code=status.HTTP_303_SEE_OTHER)
def redirect_to_long_url(short_url_token: str):
    try:
        short_url_object = ActiveShortUrl.objects(
            short_url=short_url_token
        ).get()
    except DoesNotExist:
        raise HTTPException(404, detail="Short Url not found")
    if not short_url_object.validate_link():
        raise HTTPException(422, detail='Link no longer available')
    short_url_object.redirects_count += 1
    short_url_object.save()
    return short_url_object.long_url


@router.get(
    '/analytics/{short_url_token}', response_model=ShortnerUrlAnalyticsSchema
)
def analytics(short_url_token: str):
    try:
        short_url_object = ShortUrl.objects(
            short_url=short_url_token
        ).get()
        short_url_object.validate_link()
    except DoesNotExist:
        raise HTTPException(404, detail="Short Url not found")
    return short_url_object.parse_object()

from typing import Optional
from pydantic import BaseModel


class ShortnerUrlInputSchema(BaseModel):
    url: str
    custom_short_link: Optional[str] = None


class ShortnerUrlSchema(BaseModel):
    long_url: str
    short_url: str

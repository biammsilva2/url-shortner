from pydantic import BaseModel


class ShortnerUrlInputSchema(BaseModel):
    url: str


class ShortnerUrlSchema(BaseModel):
    long_url: str
    short_url: str

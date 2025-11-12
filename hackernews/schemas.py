from pydantic import BaseModel, Field


class HackerNewsItem(BaseModel):
    id: int = Field(gt=0, examples=[1])
    title: str = Field(min_length=2, max_length=128, examples=["Example Title"])
    link: str = Field(min_length=5, max_length=512, examples=["https://example.com"])

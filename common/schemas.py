from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    data: Optional[T]
    message: str = Field(min_length=1, max_length=255)
    timestamp: datetime = Field(default_factory=datetime.now)


class NewsItem(BaseModel):
    id: int = Field(gt=0, examples=[1])
    title: str = Field(min_length=2, max_length=128, examples=["Example Title"])
    url: str = Field(min_length=5, max_length=512, examples=["https://example.com"])

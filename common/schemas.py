from datetime import datetime
from typing import Generic, Optional, TypeVar, Literal
from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    data: Optional[T]
    message: str = Field(min_length=1, max_length=255)
    timestamp: datetime = Field(default_factory=datetime.now)


class NewsItem(BaseModel):
    id: int = Field(gt=0, examples=[1])
    title: str = Field(min_length=2, max_length=128, examples=["Example Title"])
    url: str = Field(min_length=5, max_length=512, examples=["https://example.com"])


class GeneratePodcastRequest(BaseModel):
    limit: int = Field(gt=0, le=10, default=3, examples=[3])
    filename_prefix: str = Field(
        min_length=1, max_length=32, default="podcast_", examples=["hackernews_", "geeknews_"], alias="filenamePrefix"
    )
    text_model: Literal["gpt-4.1-mini", "gpt-4.1"] = Field(alias="textModel")
    tts_model: Literal["gemini-2.5-flash-tts", "gemini-2.5-pro-tts"] = Field(alias="ttsModel")

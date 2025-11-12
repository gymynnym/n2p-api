from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    data: Optional[T]
    message: str = Field(min_length=1, max_length=255)
    timestamp: datetime = Field(default_factory=datetime.now)

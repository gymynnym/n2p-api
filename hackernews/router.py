from fastapi import APIRouter, Depends, Query
from common.depends import get_redis
from common.schemas import ResponseModel
from starlette import status
from redis import asyncio as aioredis
from hackernews.schemas import HackerNewsItem
from hackernews import service as hackernews_service, messages as hackernews_messages


router = APIRouter(prefix="/hackernews", tags=["HackerNews"])


@router.get("/top", response_model=ResponseModel[list[HackerNewsItem]], status_code=status.HTTP_200_OK)
async def get_top_items(
    r: aioredis.Redis = Depends(get_redis),
    limit: int = Query(gt=0, default=20),
    page: int = Query(gt=0, default=1),
):
    data = await hackernews_service.get_top_items(r, limit, page)
    return ResponseModel(
        data=data,
        message=hackernews_messages.GET_SUCCESS,
    )

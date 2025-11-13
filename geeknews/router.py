from fastapi import APIRouter, Depends, Query
from common.depends import get_redis
from common.schemas import ResponseModel, NewsItem
from starlette import status
from redis import asyncio as aioredis
from geeknews import service as geeknews_service, messages as geeknews_messages, lifespan as geeknews_lifespan


router = APIRouter(prefix="/geeknews", tags=["GeekNews"], lifespan=geeknews_lifespan.lifespan)


@router.get("/top", response_model=ResponseModel[list[NewsItem]], status_code=status.HTTP_200_OK)
async def get_top_items(
    r: aioredis.Redis = Depends(get_redis),
    limit: int = Query(gt=0, default=20),
    page: int = Query(gt=0, default=1),
):
    data = await geeknews_service.get_top_items(r, limit, page)
    return ResponseModel(
        data=data,
        message=geeknews_messages.GET_SUCCESS,
    )

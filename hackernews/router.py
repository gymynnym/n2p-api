from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from common.depends import get_redis
from common.schemas import GeneratePodcastRequest, ResponseModel, NewsItem
from starlette import status
from redis import asyncio as aioredis
from hackernews import service as hackernews_service, messages as hackernews_messages, lifespan as hackernews_lifespan
from podcast import service as podcast_service


router = APIRouter(prefix="/hackernews", tags=["HackerNews"], lifespan=hackernews_lifespan.lifespan)


@router.get("/top", response_model=ResponseModel[list[NewsItem]], status_code=status.HTTP_200_OK)
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


@router.post("/podcasts/generate", status_code=status.HTTP_201_CREATED)
async def generate_podcast(request: GeneratePodcastRequest, r: aioredis.Redis = Depends(get_redis)):
    urls = await hackernews_service.get_top_item_urls(r, request.limit)
    data = podcast_service.generate_podcast(
        r=r,
        urls=urls,
        **request.model_dump(exclude={"limit"}),
        redis_key=hackernews_service.HACKERNEWS_PODCASTS_KEY,
    )
    headers = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    return StreamingResponse(data, media_type="text/plain", headers=headers)

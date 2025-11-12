from redis import asyncio as aioredis
from hackernews.schemas import HackerNewsItem


HACKERNEWS_REDIS_KEY = "hackernews:items"


async def get_top_items(r: aioredis.Redis, limit: int, page: int) -> HackerNewsItem:
    start, end = (page - 1) * limit, page * limit - 1
    redis_data = await r.zrevrange(HACKERNEWS_REDIS_KEY, start, end)
    data = list(map(lambda item: HackerNewsItem.model_validate_json(item), redis_data))
    return data

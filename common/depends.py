from fastapi import Request
from redis import asyncio as aioredis


def get_redis(request: Request) -> aioredis.Redis:
    return request.app.state.redis

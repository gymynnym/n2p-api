from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis import asyncio as aioredis
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = os.environ["REDIS_URL"]
    r = aioredis.from_url(redis_url, decode_responses=True)
    try:
        await r.ping()
    except aioredis.ConnectionError as e:
        raise RuntimeError(f"Failed to connect to Redis: {e}")

    app.state.redis = r

    try:
        yield
    finally:
        await r.close()
        await r.connection_pool.disconnect(inuse_connections=True)

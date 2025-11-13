from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from hackernews import service as hackernews_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=hackernews_service.scrap_items,
        trigger="interval",
        seconds=3600,  # 1 hour
        args=[app.state.redis],
    )
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown()

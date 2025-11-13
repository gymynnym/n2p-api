from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from geeknews import service as geeknews_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        func=geeknews_service.scrap_items,
        trigger="interval",
        seconds=3600,  # 1 hour
        args=[app.state.redis],
    )
    scheduler.start()
    try:
        yield
    finally:
        scheduler.shutdown()

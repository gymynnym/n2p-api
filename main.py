from fastapi import FastAPI
from lifespan import lifespan
from hackernews.router import router as hackernews_router
from geeknews.router import router as geeknews_router
from podcast.router import router as podcast_router
from starlette.middleware.cors import CORSMiddleware
import os


app = FastAPI(lifespan=lifespan)
app.include_router(hackernews_router)
app.include_router(geeknews_router)
app.include_router(podcast_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ["CLIENT_HOST"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization"],
)

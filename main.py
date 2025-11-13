from fastapi import FastAPI
from lifespan import lifespan
from hackernews.router import router as hackernews_router
from starlette.middleware.cors import CORSMiddleware
import os


app = FastAPI(lifespan=lifespan)
app.include_router(hackernews_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ["CLIENT_HOST"]],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization"],
)


@app.get("/")
def say_hello():
    return "Hello, World!"

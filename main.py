from fastapi import FastAPI
from lifespan import lifespan
from hackernews.router import router as hackernews_router


app = FastAPI(lifespan=lifespan)
app.include_router(hackernews_router)


@app.get("/")
def say_hello():
    return "Hello, World!"

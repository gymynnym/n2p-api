from fastapi import FastAPI
from lifespan import lifespan


app = FastAPI(lifespan=lifespan)


@app.get("/")
def say_hello():
    return "Hello, World!"

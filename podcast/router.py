from fastapi import APIRouter, Depends, Path
from fastapi.responses import FileResponse
from common.depends import get_redis
from common.schemas import ResponseModel
from starlette import status
from podcast import service as podcast_service
from redis import asyncio as aioredis


router = APIRouter(prefix="/podcasts", tags=["Podcasts"])

filename_param = Path(
    regex=r"^[^/]+$",
    max_length=255,
    description="The filename of the podcast without extension",
)


@router.get("/{filename}.txt", response_model=ResponseModel[str], status_code=status.HTTP_200_OK)
async def get_podcast_text(filename: str = filename_param):
    filepath = await podcast_service.get_podcast_filepath(f"{filename}.txt")
    return FileResponse(
        path=filepath,
        filename=f"{filename}.txt",
        media_type="application/octet-stream",
    )


@router.get("/{filename}.mp3", status_code=status.HTTP_200_OK)
async def get_podcast_audio(filename: str = filename_param):
    filepath = await podcast_service.get_podcast_filepath(f"{filename}.mp3")
    return FileResponse(
        path=filepath,
        filename=f"{filename}.mp3",
        media_type="application/octet-stream",
    )


@router.delete("/{filename}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_podcast(filename: str = filename_param, r: aioredis.Redis = Depends(get_redis)):
    await podcast_service.delete_podcast(r, filename)
    return
